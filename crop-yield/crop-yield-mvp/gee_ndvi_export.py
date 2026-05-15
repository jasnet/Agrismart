"""
gee_ndvi_export.py
- Reads data/fields.geojson
- For a date range, computes NDVI time series from Sentinel-2 SR
- Exports zonal stats per field to outputs/ndvi_zonal_stats.csv
"""

import ee
import geopandas as gpd
import pandas as pd
import time
import json
from shapely.geometry import mapping

# --------------- CONFIG ---------------
START_DATE = '2024-10-01'   # change to your season start
END_DATE   = '2025-04-30'   # change to season end
SCALE = 10                  # meters
OUTPUT_CSV = 'outputs/ndvi_zonal_stats.csv'
FIELD_GEOJSON = 'data/fields.geojson'
# Optional: filter clouds threshold
MAX_CLOUD_PCT = 30
# --------------------------------------

def init_ee():
    try:
        ee.Initialize()
        print("Earth Engine initialized (default).")
    except Exception as e:
        print("Could not initialize Earth Engine automatically. If using a service account, "
              "set up credentials. Error:", e)
        raise

def sentinel2_collection(start, end):
    col = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterDate(start, end) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', MAX_CLOUD_PCT)) \
            .select(['B4', 'B8'])  # B4 = red, B8 = NIR
    return col

def add_ndvi(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return image.addBands(ndvi)

def compute_zonal_stats(geom, img_coll):
    # reduce collection to list of images (sample every 10 days via composite)
    def process_image(img):
        img = ee.Image(img)
        ndvi = img.select('NDVI')
        stats = ndvi.reduceRegion(
            reducer=ee.Reducer.mean().combine(ee.Reducer.max(), '', True),
            geometry=geom,
            scale=SCALE,
            bestEffort=True,
            maxPixels=1e9
        )
        # attach date
        date = img.date().format('YYYY-MM-dd')
        return ee.Feature(None, stats.set({'date': date}))
    feat_list = img_coll.map(add_ndvi).map(process_image).filter(ee.Filter.notNull(['NDVI_mean']))
    return feat_list

def main():
    init_ee()
    fields = gpd.read_file(FIELD_GEOJSON)
    results = []

    col = sentinel2_collection(START_DATE, END_DATE)
    # reduce to median per 10-day windows to limit items (practical for MVP)
    # We'll create a list of date ranges and compute median composites
    start = pd.to_datetime(START_DATE)
    end = pd.to_datetime(END_DATE)
    window_days = 10
    windows = []
    cur = start
    while cur <= end:
        w_end = min(cur + pd.Timedelta(days=window_days-1), end)
        windows.append((cur.strftime('%Y-%m-%d'), w_end.strftime('%Y-%m-%d')))
        cur += pd.Timedelta(days=window_days)

    for idx, row in fields.iterrows():
        fid = row.get('field_id') or f'field_{idx:03d}'
        geom = mapping(row.geometry)
        ee_geom = ee.Geometry(geom)
        field_stats = []
        for s,e in windows:
            comp = col.filterDate(s, e).median()
            comp = add_ndvi(comp)
            stat = comp.select('NDVI').reduceRegion(
                reducer=ee.Reducer.mean().combine(ee.Reducer.max(), '', True),
                geometry=ee_geom,
                scale=SCALE,
                bestEffort=True,
                maxPixels=1e9
            )
            stat_dict = stat.getInfo()
            mean = stat_dict.get('NDVI_mean')
            maxv = stat_dict.get('NDVI_max')
            if mean is None:
                continue
            field_stats.append({
                'field_id': fid,
                'start': s,
                'end': e,
                'ndvi_mean': mean,
                'ndvi_max': maxv
            })
            time.sleep(0.1)  # gentle throttling

        # aggregate across windows into summary features
        if field_stats:
            df = pd.DataFrame(field_stats)
            results.append({
                'field_id': fid,
                'ndvi_mean_season': df['ndvi_mean'].mean(),
                'ndvi_max_season': df['ndvi_max'].max(),
                'ndvi_auc_approx': df['ndvi_mean'].sum(),   # simple proxy for area under curve
                'n_windows': len(df)
            })

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_CSV, index=False)
    print("Saved zonal stats to", OUTPUT_CSV)

if __name__ == '__main__':
    main()

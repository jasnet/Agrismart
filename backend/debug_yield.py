import sys
import os
from pathlib import Path
import joblib
import pandas as pd
import json

# Mimic the logic in main.py
BASE_DIR = Path(os.getcwd())
print(f"BASE_DIR: {BASE_DIR}")

def test_yield_data():
    try:
        # Define paths
        project_root = BASE_DIR.parent
        mvp_dir = project_root / "crop-yield" / "crop-yield-mvp"
        
        print(f"MVP Dir: {mvp_dir}")
        
        model_path = mvp_dir / "outputs" / "model.joblib"
        ndvi_path = mvp_dir / "outputs" / "ndvi_zonal_stats.csv"
        soil_path = mvp_dir / "data" / "soil_and_ops.csv"
        fields_path = mvp_dir / "data" / "fields.geojson"
        
        print(f"Model Path: {model_path} (Exists: {model_path.exists()})")
        print(f"NDVI Path: {ndvi_path} (Exists: {ndvi_path.exists()})")
        print(f"Soil Path: {soil_path} (Exists: {soil_path.exists()})")
        print(f"Fields Path: {fields_path} (Exists: {fields_path.exists()})")
        
        if not model_path.exists():
            print("Error: Model not found")
            return
            
        # Load data
        print("Loading model...")
        model_bundle = joblib.load(model_path)
        model = model_bundle['model']
        features = model_bundle['features']
        print("Model loaded.")
        
        print("Loading CSVs...")
        ndvi_df = pd.read_csv(ndvi_path)
        soil_df = pd.read_csv(soil_path)
        print("CSVs loaded.")
        
        # Load fields to get crop type
        print("Loading GeoJSON...")
        with open(fields_path, 'r') as f:
            geojson = json.load(f)
        
        field_props = []
        for feature in geojson['features']:
            props = feature['properties']
            field_props.append(props)
        fields_df = pd.DataFrame(field_props)
        
        # Merge
        print("Merging data...")
        merged = fields_df.merge(ndvi_df, on='field_id', how='left')
        merged = merged.merge(soil_df, on='field_id', how='left')
        merged = merged.fillna(0)
        
        # Predict
        print("Predicting...")
        X = merged[features]
        merged['pred_yield'] = model.predict(X)
        print("Prediction successful.")
        print(merged[['field_id', 'pred_yield']])

    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_yield_data()

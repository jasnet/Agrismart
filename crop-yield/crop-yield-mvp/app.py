# app.py
import streamlit as st
import geopandas as gpd
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="Crop Yield MVP")

st.title("Crop Yield MVP Dashboard")

# Load data
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
fields_path = os.path.join(BASE_DIR, 'data', 'fields.geojson')
model_path = os.path.join(BASE_DIR, 'outputs', 'model.joblib')
ndvi_csv = os.path.join(BASE_DIR, 'outputs', 'ndvi_zonal_stats.csv')
soil_csv = os.path.join(BASE_DIR, 'data', 'soil_and_ops.csv')

fields = gpd.read_file(fields_path)
with st.sidebar.expander("📂 File Paths", expanded=False):
    st.write(f"**Fields:** `{os.path.basename(fields_path)}`")
    st.write(f"**NDVI:** `{os.path.basename(ndvi_csv)}`")
    st.write(f"**Model:** `{os.path.basename(model_path)}`")
    st.caption(f"📍 Location: `{os.path.basename(BASE_DIR)}/`")

# Initialize session state
if 'model' not in st.session_state:
    st.session_state['model'] = None
    st.session_state['features'] = []
    st.session_state['merged_data'] = None
    st.session_state['data_loaded'] = False

def load_all_data():
    """Loads model and data, merges them, and updates session state."""
    # 1. Load Model
    try:
        model_bundle = joblib.load(model_path)
        st.session_state['model'] = model_bundle['model']
        st.session_state['features'] = model_bundle['features']
    except Exception as e:
        st.error(f"Could not load model: {e}")
        st.session_state['model'] = None
        st.session_state['features'] = []

    # 2. Load NDVI
    try:
        ndvi = pd.read_csv(ndvi_csv)
    except Exception as e:
        st.error(f"Could not load NDVI CSV: {e}")
        ndvi = pd.DataFrame()

    # 3. Merge Data
    if 'field_id' in fields.columns:
        # Start with fields
        pred_df = fields[['field_id']].copy()
        
        # Merge NDVI
        if not ndvi.empty:
            pred_df = pred_df.merge(ndvi, on='field_id', how='left')
        
        # Merge Soil
        try:
            soil_df = pd.read_csv(soil_csv)
            pred_df = pred_df.merge(soil_df, on='field_id', how='left')
        except Exception as e:
            st.warning(f"Could not load soil data: {e}")

        pred_df = pred_df.fillna(0)
        
        # 4. Predict
        model = st.session_state['model']
        features = st.session_state['features']
        
        if model and features:
            missing_cols = [c for c in features if c not in pred_df.columns]
            if missing_cols:
                st.error(f"Missing features: {missing_cols}")
                st.write("Available:", pred_df.columns.tolist())
            else:
                X = pred_df[features]
                preds = model.predict(X)
                pred_df['pred_yield'] = preds
        else:
            pred_df['pred_yield'] = 0.0

        # Final Merge for Display
        # Merge predictions back to the main fields geodataframe
        final_merged = fields.merge(pred_df[['field_id'] + [c for c in pred_df.columns if c not in fields.columns and c != 'field_id']], on='field_id', how='left')
        st.session_state['merged_data'] = final_merged
        st.session_state['data_loaded'] = True

# Load on startup if not loaded
if not st.session_state['data_loaded']:
    load_all_data()

if st.sidebar.button("Refresh Data & Model"):
    load_all_data()
    st.success("Data refreshed!")

# --- UI RENDER ---
# --- UI RENDER ---
merged = st.session_state['merged_data']

if merged is not None:
    # 1. Summary Metrics
    st.markdown("### 📊 Overview")
    c1, c2, c3, c4 = st.columns(4)
    
    avg_yield = merged['pred_yield'].mean() if 'pred_yield' in merged.columns else 0
    avg_ndvi = merged['ndvi_mean_season'].mean() if 'ndvi_mean_season' in merged.columns else 0
    total_fields = len(merged)
    
    c1.metric("Total Fields", total_fields)
    c2.metric("Avg Predicted Yield", f"{avg_yield:.2f} t/ha")
    c3.metric("Avg NDVI", f"{avg_ndvi:.2f}")
    
    # 2. Main Content Layout
    col_map, col_data = st.columns([3, 2])
    
    with col_map:
        st.subheader("🗺️ Field Map")
        # Centering
        if not merged.geometry.is_empty.all():
            lat = merged.geometry.centroid.y.mean()
            lon = merged.geometry.centroid.x.mean()
        else:
            lat, lon = 20.0, 78.0

        m = folium.Map(location=[lat, lon], zoom_start=13, tiles="CartoDB positron")
        
        for _, r in merged.iterrows():
            if r.geometry is None: continue
            sim_geo = r.geometry.__geo_interface__
            yld = r.get('pred_yield', 0)
            field_id = r.get('field_id', 'Unknown')
            crop = r.get('crop_type', 'N/A')
            
            popup_msg = f"""
            <b>Field:</b> {field_id}<br>
            <b>Crop:</b> {crop}<br>
            <b>Yield:</b> {yld:.2f} t/ha
            """
            
            folium.GeoJson(
                sim_geo,
                tooltip=f"{field_id}: {yld:.1f} t/ha",
                popup=folium.Popup(popup_msg, max_width=300),
                style_function=lambda x, val=yld: {
                    'fillColor': '#2ca02c' if val > 9 else '#8cbf3f' if val > 8 else '#d4d925' if val > 0 else '#7f7f7f',
                    'color': 'black',
                    'weight': 2,
                    'fillOpacity': 0.7
                }
            ).add_to(m)

        st_folium(m, width=None, height=500, use_container_width=True)

    with col_data:
        st.subheader("📋 Field Details")
        
        # Select columns to display
        display_cols = ['field_id', 'crop_type', 'pred_yield', 'ndvi_mean_season', 'soil_ph']
        final_cols = [c for c in display_cols if c in merged.columns]
        
        display_df = merged[final_cols].copy()
        
        column_config = {
            'field_id': 'Field ID',
            'crop_type': 'Crop',
            'pred_yield': st.column_config.NumberColumn('Yield (t/ha)', format="%.2f"),
            'ndvi_mean_season': st.column_config.NumberColumn('NDVI', format="%.2f"),
            'soil_ph': st.column_config.NumberColumn('pH', format="%.1f")
        }
        
        st.dataframe(
            display_df, 
            column_config=column_config, 
            use_container_width=True, 
            hide_index=True,
            height=500
        )

    # 3. Analysis Section
    st.markdown("---")
    st.subheader("📈 Analysis")
    ac1, ac2 = st.columns(2)
    
    with ac1:
        st.markdown("**Yield Distribution**")
        if 'pred_yield' in merged.columns:
            st.bar_chart(merged.set_index('field_id')['pred_yield'])
            
    with ac2:
        st.markdown("**Model Feature Importance**")
        model = st.session_state['model']
        features = st.session_state['features']
        if model:
            try:
                imp = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
                st.bar_chart(imp, color="#2ca02c")
            except:
                st.info("Feature importance not available.")

else:
    st.info("👈 Click 'Refresh Data & Model' in the sidebar to load data.")


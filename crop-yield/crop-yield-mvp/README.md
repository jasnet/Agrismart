# Crop Yield MVP

This project aims to predict crop yield using satellite data (NDVI) and farm operation records.

## Structure

- `data/`: Input data (field boundaries, soil tests, planting dates).
- `outputs/`: Generated files (NDVI stats, trained model, metrics).
- `gee_ndvi_export.py`: Script to fetch NDVI data from Google Earth Engine.
- `train_model.py`: Script to train the machine learning model.
- `app.py`: Flask API to serve the model predictions.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run NDVI export (requires GEE authentication):
   ```bash
   python gee_ndvi_export.py
   ```

3. Train the model:
   ```bash
   python train_model.py
   ```

4. Run the API:
   ```bash
   python app.py
   ```

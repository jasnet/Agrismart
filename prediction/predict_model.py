"""
predict_model.py
A small script to test the saved multi-model artifact.

Run:
  python predict_model.py
"""

import os
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "fertility_model_multi.joblib")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"{MODEL_PATH} not found. Run train_model.py first.")

payload = joblib.load(MODEL_PATH)
pipeline_crop = payload["pipeline_crop"]
pipeline_cat = payload.get("pipeline_category", None)
meta = payload.get("meta", {})
features = meta.get("features", pipeline_crop.named_steps["pre"].transformers_[0][2])

print("Features used:", features)
print("Crop target column:", meta.get("crop_target"))
print("Category column:", meta.get("category_column"))

# --- sample input: replace with real numbers ---
sample = {}
# create sample dict with feature names (if you omit some, they will be set to NaN)
for f in features:
    sample[f] = None

# fill some example values (adjust to realistic values)
if len(features) >= 3:
    sample[features[0]] = 90
    sample[features[1]] = 42
    sample[features[2]] = 43
# optionally add other numbers
for i, f in enumerate(features):
    if sample[f] is None:
        sample[f] = np.nan

df = pd.DataFrame([sample], columns=features)
print("Input row:")
print(df)

pred_crop = pipeline_crop.predict(df)[0]
conf_crop = pipeline_crop.predict_proba(df).max(axis=1)[0] if hasattr(pipeline_crop, "predict_proba") else None

print("Predicted crop:", pred_crop, " confidence:", conf_crop)

if pipeline_cat:
    pred_cat = pipeline_cat.predict(df)[0]
    conf_cat = pipeline_cat.predict_proba(df).max(axis=1)[0] if hasattr(pipeline_cat, "predict_proba") else None
    print("Predicted category:", pred_cat, " confidence:", conf_cat)

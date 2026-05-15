"""
train_model.py
Trains two pipelines:
  - pipeline_crop -> predicts crop label (common names: label|crop|crop_name)
  - pipeline_cat  -> predicts category (column name: category) [if present]

Saves a single artifact to backend/models/fertility_model_multi.joblib

Run:
  cd project-root/backend
  python -m venv venv          # optional
  source venv/bin/activate     # or venv\Scripts\activate on Windows
  pip install -r requirements.txt
  python train_model.py
"""

import os
import glob
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUT_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(OUT_DIR, exist_ok=True)

# 1) find CSV - look in current directory instead of data/ subdirectory
csv_files = glob.glob(os.path.join(BASE_DIR, "*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {BASE_DIR}. Place your CSV files there.")
csv_path = csv_files[0]
print("Using CSV:", csv_path)

# 2) load
df = pd.read_csv(csv_path)
print("Loaded shape:", df.shape)
print("Columns:", list(df.columns))

# 3) normalize column names
df.columns = [c.strip() for c in df.columns]
cols_lower = {c: c.lower() for c in df.columns}
df = df.rename(columns=cols_lower)

# 4) detect targets
# crop target candidates
crop_candidates = ['label', 'crop', 'crop_name', 'target']
crop_target = None
for c in crop_candidates:
    if c in df.columns:
        crop_target = c
        break

# category target
category_column = 'category' if 'category' in df.columns else None

if crop_target is None:
    raise RuntimeError("No crop target column found. Expected one of: " + ", ".join(crop_candidates))

print("Detected crop target:", crop_target)
print("Detected category column:", category_column)

# 5) detect features
expected_features = ['n', 'p', 'k', 'temperature', 'temp', 'humidity', 'ph', 'rainfall', 'rain_fall', 'rainfall_mm']
# prefer typical N,P,K etc (lowercase). We'll pick the best numeric set available.
available_cols = df.columns.tolist()

# collect features if they exist
chosen = []
for ef in expected_features:
    if ef in available_cols and ef not in (crop_target, category_column):
        # avoid duplicate if 'temp' and 'temperature' both exist: prefer 'temperature' first
        if ef in ('temp',) and 'temperature' in available_cols:
            continue
        chosen.append(ef)

# if not enough found, fallback to numeric columns excluding targets
if len(chosen) < 3:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in (crop_target, category_column)]
    # if numeric columns found, use them
    chosen = numeric_cols

if not chosen:
    raise RuntimeError("No numeric feature columns detected. Ensure the CSV contains numeric columns for features.")

# choose up to 7 features (order will be saved in meta)
features = chosen[:7]
print("Using features:", features)

# 6) Preprocessing: coerce numeric, drop rows missing labels, impute features
# convert features to numeric (strip non-numeric chars)
for c in features:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(r"[^\d\.\-]", "", regex=True), errors='coerce')

# drop rows missing crop target
df = df.dropna(subset=[crop_target])
# ensure category rows present (if category exists, drop rows missing category too)
if category_column:
    df = df.dropna(subset=[category_column])

# simple median imputer (pipeline will re-impute for safety)
X = df[features].copy()
y_crop = df[crop_target].astype(str).copy()
y_cat = df[category_column].astype(str).copy() if category_column else None

# pipeline for numeric features
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, features)
])

# two classifiers (same architecture)
clf_crop = Pipeline([
    ("pre", preprocessor),
    ("rf", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))
])

clf_cat = None
if category_column:
    clf_cat = Pipeline([
        ("pre", preprocessor),
        ("rf", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))
    ])

# 7) Train/test split and fit
print("Splitting and training...")
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_crop, test_size=0.2, stratify=y_crop, random_state=42)
clf_crop.fit(X_train_c, y_train_c)
y_pred_crop = clf_crop.predict(X_test_c)

print("Crop classification report:")
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
print(f"Accuracy:  {accuracy_score(y_test_c, y_pred_crop):.4f}")
print(f"Precision: {precision_score(y_test_c, y_pred_crop, average='weighted'):.4f}")
print(f"Recall:    {recall_score(y_test_c, y_pred_crop, average='weighted'):.4f}")
print(f"F1 Score:  {f1_score(y_test_c, y_pred_crop, average='weighted'):.4f}")
print(classification_report(y_test_c, y_pred_crop))
print("Crop confusion matrix:")
print(confusion_matrix(y_test_c, y_pred_crop))

if clf_cat:
    # For category, use only rows where category is present (we already dropped NA)
    X_train_cat, X_test_cat, y_train_cat, y_test_cat = train_test_split(X, y_cat, test_size=0.2, stratify=y_cat, random_state=42)
    clf_cat.fit(X_train_cat, y_train_cat)
    y_pred_cat = clf_cat.predict(X_test_cat)
    print("Category classification report:")
    print(classification_report(y_test_cat, y_pred_cat))
    print("Category confusion matrix:")
    print(confusion_matrix(y_test_cat, y_pred_cat))

# 8) Save artifact: a dict with both pipelines and metadata
artifact = {
    "pipeline_crop": clf_crop,
    "pipeline_category": clf_cat,   # may be None if no category found
    "meta": {
        "features": features,
        "crop_target": crop_target,
        "category_column": category_column
    }
}

out_path = os.path.join(OUT_DIR, "fertility_model_multi.joblib")
joblib.dump(artifact, out_path)
print("Saved artifact to:", out_path)

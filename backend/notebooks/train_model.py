
import os
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"

# ---------- 1. Load CSV ----------
csv_path = DATA_DIR / "Crop_recommendation.csv"
df = pd.read_csv(csv_path)

# ---------- 2. Normalize column names: strip spaces & lowercase ----------
df.columns = [c.strip() for c in df.columns]          # remove surrounding spaces
# keep original mapping if you want, but convert to lower for robustness
cols_lower = {c: c.lower() for c in df.columns}
df = df.rename(columns=cols_lower)

print("Columns after normalization:", list(df.columns))

# ---------- 3. Decide X and y based on your CSV ----------
# From the file you uploaded, columns are: N, P, K, temperature, humidity, ph, rainfall, label
# after lowercasing they become: 'n','p','k','temperature','humidity','ph','rainfall','label'
expected_features = ['n','p','k','temperature','humidity','ph','rainfall']
target_col = 'label'   # your file uses 'label' as crop target

# check that required columns exist
missing = [c for c in expected_features + [target_col] if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns in CSV: {missing}. Check column names in the CSV or the normalization above.")

# ---------- 4. Basic cleaning / type conversion ----------
# Convert numeric columns to numeric, coerce errors to NaN
for c in expected_features:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Simple missing-value summary
print("Missing values per column:\n", df[expected_features + [target_col]].isnull().sum())

# For demo: drop rows where target is missing
df = df.dropna(subset=[target_col])
# For features: simple imputation of numeric missing values with median
num_imputer = SimpleImputer(strategy='median')
df[expected_features] = num_imputer.fit_transform(df[expected_features])

# ---------- 5. Prepare X and y ----------
X = df[expected_features].copy()
y = df[target_col].astype(str).copy()  # ensure string labels

# If you later want to predict fertility_class instead of crop label, change target_col accordingly.

# ---------- 6. Pipeline + ColumnTransformer ----------
# There are no categorical features among expected_features; if you later include soil_type, handle that.
numeric_features = expected_features  # all numeric here
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),   # safety
    ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    # If you add categorical columns later, add an ('cat', OneHotEncoder(...), cat_features) entry
])

clf = Pipeline(steps=[
    ('pre', preprocessor),
    ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# ---------- 7. Train/test split and fit ----------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)
clf.fit(X_train, y_train)
score = clf.score(X_test, y_test)
print(f"Test accuracy: {score:.4f}")

# ---------- 8. Save model ----------
MODELS_DIR.mkdir(exist_ok=True)
model_path = MODELS_DIR / "fertility_model.joblib"
joblib.dump(clf, model_path)
print(f"Saved model to {model_path}")

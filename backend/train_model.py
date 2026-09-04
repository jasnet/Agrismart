import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Ensure models dir exists
(BASE_DIR / "models").mkdir(exist_ok=True)

# Load data
print("Loading data...")
try:
    data = pd.read_csv(BASE_DIR / "data" / "Crop_recommendation.csv")
except FileNotFoundError:
    print(f"Error: {BASE_DIR / 'data' / 'Crop_recommendation.csv'} not found.")
    exit(1)

# Features and Label
# Ensure strict column selection from CSV
required_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
missing = [c for c in required_columns if c not in data.columns]
if missing:
    print(f"Error: Missing columns in CSV: {missing}")
    # Try lowercase fallback if needed, but assuming CSV matched head output
    exit(1)

X = data[required_columns]
y = data['label']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train
print("Training model...")
pipeline.fit(X_train, y_train)
print("Validation Score:", pipeline.score(X_test, y_test))

# Save
model_path = BASE_DIR / "models" / "fertility_model.joblib"
joblib.dump(pipeline, model_path)
print(f"Model saved to {model_path}")

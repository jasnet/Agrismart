import joblib
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
model_path = PROJECT_ROOT / "models" / "fertility_model.joblib"

if not model_path.exists():
    raise FileNotFoundError(f"{model_path} not found. Train your model first.")

clf = joblib.load(model_path)

# ---------- Define feature column names ----------
# These must match exactly what you used during training:
feature_cols = ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall']

# ---------- Take one example input ----------
# Replace the numbers below with your real values
sample = {
    'n': 90,
    'p': 42,
    'k': 43,
    'temperature': 25.5,
    'humidity': 80.0,
    'ph': 6.5,
    'rainfall': 200.0
}

# Convert to DataFrame (this fixes the error you saw)
sample_df = pd.DataFrame([sample])  # 1 row, with column names

# ---------- Predict ----------
prediction = clf.predict(sample_df)
print("Predicted crop:", prediction[0])

"""
predict_fertilizer.py
Loads the trained fertilizer model and predicts for a sample input.
"""

import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "fertilizer_model.joblib")

def predict():
    if not os.path.exists(MODEL_PATH):
        print(f"Model not found at {MODEL_PATH}. Run train_fertilizer.py first.")
        return

    print(f"Loading model from {MODEL_PATH}...")
    model = joblib.load(MODEL_PATH)
    
    # Sample Input (matches the columns expected by the model)
    # Temparature, Humidity, Moisture, Nitrogen, Potassium, Phosphorous, Soil Type, Crop Type
    sample_input = {
        "Temparature": [30],
        "Humidity": [60],
        "Moisture": [40],
        "Nitrogen": [10],
        "Potassium": [10],
        "Phosphorous": [10],
        "Soil Type": ["Sandy"],
        "Crop Type": ["Maize"]
    }
    
    df = pd.DataFrame(sample_input)
    print("\nInput Data:")
    print(df)
    
    print("\nPredicting...")
    prediction = model.predict(df)
    print(f"Predicted Fertilizer: {prediction[0]}")
    
    # Probabilities (optional)
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(df)
        print(f"Confidence: {probs.max():.2f}")

if __name__ == "__main__":
    predict()

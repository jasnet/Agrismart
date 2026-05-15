import tensorflow as tf
from pathlib import Path
import os

BASE_DIR = Path(".").resolve()
MODEL_PATH = BASE_DIR / "models" / "trained_model.keras"

print(f"Checking model at: {MODEL_PATH}")

if not MODEL_PATH.exists():
    print("Model file does not exist!")
else:
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print("Model loaded successfully!")
        model.summary()
    except Exception as e:
        print(f"Error loading model: {e}")

import sys
import pickle
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

# Get arguments
temp = float(sys.argv[1])
hum = float(sys.argv[2])
rain = int(sys.argv[3])

# Load model
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Predict
prediction = model.predict([[temp, hum, rain]])

# Output JSON
import json
print(json.dumps([{"irrigate": int(prediction[0])}]))

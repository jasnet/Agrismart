import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# Sample training data
data = {
    "temperature": [25, 30, 35, 28, 40, 22, 33],
    "humidity": [70, 50, 30, 60, 20, 80, 40],
    "rain": [1, 0, 0, 0, 0, 1, 0],
    "irrigate": [0, 1, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

X = df[["temperature", "humidity", "rain"]]
y = df["irrigate"]

model = LogisticRegression()
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("ML Model trained and saved")

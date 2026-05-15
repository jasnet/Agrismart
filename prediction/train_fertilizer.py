"""
train_fertilizer.py
Trains a Random Forest Classifier for Fertilizer Prediction.
Uses 'Fertilizer Prediction.csv' as input.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "Fertilizer Prediction.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "fertilizer_model.joblib")

def train():
    print(f"Loading data from {DATA_FILE}...")
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"{DATA_FILE} not found.")
    
    df = pd.read_csv(DATA_FILE)
    
    # Normalize column names
    df.columns = [c.strip() for c in df.columns]
    
    # Target column
    target_col = "Fertilizer Name"
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in CSV.")
    
    # Features
    numeric_features = ["Temparature", "Humidity", "Moisture", "Nitrogen", "Potassium", "Phosphorous"]
    categorical_features = ["Soil Type", "Crop Type"]
    
    # Check if all features exist
    missing_cols = [c for c in numeric_features + categorical_features if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in CSV: {missing_cols}")
    
    X = df[numeric_features + categorical_features]
    y = df[target_col]
    
    print("Features:", numeric_features + categorical_features)
    print("Target:", target_col)
    
    # Preprocessing Pipeline
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # Model Pipeline
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))])
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training model...")
    clf.fit(X_train, y_train)
    
    # Evaluation
    # Evaluation
    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)
    
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

    print("--- Performance Metrics ---")
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred, average='weighted'):.4f} (Weighted)")
    print(f"Recall:    {recall_score(y_test, y_pred, average='weighted'):.4f} (Weighted)")
    print(f"F1 Score:  {f1_score(y_test, y_pred, average='weighted'):.4f} (Weighted)")
    
    try:
        auc = roc_auc_score(y_test, y_proba, multi_class='ovr', average='weighted')
        print(f"AUC (OvR): {auc:.4f}")
    except Exception as e:
        print(f"AUC not calculated: {e}")

    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    # Save Model
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(clf, MODEL_PATH)
    print("Done.")

if __name__ == "__main__":
    train()

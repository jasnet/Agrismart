# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import lightgbm as lgb
import joblib
import json
import os

NDVI_CSV = 'outputs/ndvi_zonal_stats.csv'
SOIL_CSV = 'data/soil_and_ops.csv'   # optional, merge if exists
MODEL_OUT = 'outputs/model.joblib'
METRICS_OUT = 'outputs/metrics.json'

def load_data():
    ndvi = pd.read_csv(NDVI_CSV)
    if os.path.exists(SOIL_CSV):
        soil = pd.read_csv(SOIL_CSV)
        df = ndvi.merge(soil, on='field_id', how='left')
    else:
        df = ndvi.copy()
    # Expect user to have a 'yield_t' column in soil_and_ops.csv or merged file
    if 'yield_t' not in df.columns:
        raise ValueError("No 'yield_t' ground truth column found. Provide yield in soil_and_ops.csv or merge it.")
    # simple feature set
    features = ['ndvi_mean_season', 'ndvi_max_season', 'ndvi_auc_approx']
    # add any numeric soil features if present
    extra = [c for c in df.columns if c not in features + ['field_id', 'yield_t']]
    for c in extra:
        if pd.api.types.is_numeric_dtype(df[c]):
            features.append(c)
    df = df.dropna(subset=features + ['yield_t'])
    X = df[features].astype(float)
    y = df['yield_t'].astype(float)
    return df, X, y, features

def train_and_evaluate(X, y):
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    preds = np.zeros(len(y))
    fold = 0
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'verbosity': -1,
        'random_state': 42,
        'n_estimators': 1000,
        'learning_rate': 0.05,
        'min_child_samples': 1
    }
    models = []
    for train_idx, val_idx in kf.split(X):
        fold += 1
        Xtrain, Xval = X.iloc[train_idx], X.iloc[val_idx]
        ytrain, yval = y.iloc[train_idx], y.iloc[val_idx]
        model = lgb.LGBMRegressor(**params)
        model.fit(Xtrain, ytrain,
                  eval_set=[(Xval, yval)])
        p = model.predict(Xval, num_iteration=model.best_iteration_)
        preds[val_idx] = p
        models.append(model)
    mae = mean_absolute_error(y, preds)
    rmse = np.sqrt(mean_squared_error(y, preds))
    r2 = r2_score(y, preds)
    return models, {'mae': float(mae), 'rmse': float(rmse), 'mse': float(rmse**2), 'r2': float(r2)}

def save_ensemble(models, features):
    # Save the first model and store feature order. For small MVP this is OK.
    os.makedirs('outputs', exist_ok=True)
    joblib.dump({'model': models[0], 'features': features}, MODEL_OUT)
    print("Saved model to", MODEL_OUT)

def main():
    df, X, y, features = load_data()
    models, metrics = train_and_evaluate(X, y)
    save_ensemble(models, features)
    with open(METRICS_OUT, 'w') as f:
        json.dump(metrics, f, indent=2)
    print("Training complete. Metrics:", metrics)

if __name__ == '__main__':
    main()

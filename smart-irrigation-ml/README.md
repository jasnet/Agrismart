# Smart Irrigation ML System

This is a separate module that uses Machine Learning to decide irrigation needs based on weather data.

## Structure

- **backend/**: Node.js server with Python ML integration.
- **frontend/**: Simple HTML/JS dashboard.

## Setup

1. **Backend**:
   ```bash
   cd backend
   npm install
   # Train the model once
   python3 ml/train_model.py
   # Start server
   node server.js
   ```

2. **Frontend**:
   Open `frontend/index.html` in your browser.

## Features

- **ML Model**: Logistic Regression (Python) predicts if irrigation is needed based on Temp, Humidity, Rain.
- **Logic**: Calculates specific water requirements based on Crop type.
- **Yield**: Estimates yield based on irrigation decision.

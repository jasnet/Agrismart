#!/bin/bash

# Define paths and start commands for each service
BASE_DIR="/Applications/MCA PROJECT"

echo "Starting Backend (FastAPI) on port 8000..."
cd "$BASE_DIR/backend" && source venv/bin/activate && uvicorn main:app --port 8000 > backend.log 2>&1 &
echo $! > "$BASE_DIR/backend.pid"

echo "Starting Smart Irrigation Backend (FastAPI) on port 8001..."
cd "$BASE_DIR/smart-irrigation-backend" && source venv/bin/activate && uvicorn app.main:app --port 8001 > smart-irrigation-backend.log 2>&1 &
echo $! > "$BASE_DIR/smart-irrigation-backend.pid"

echo "Starting AgriVoiceAssistant (Flask) on port 5003..."
cd "$BASE_DIR/AgriVoiceAssistant_Flask/backend" && source venv/bin/activate && python app.py > voice_assistant.log 2>&1 &
echo $! > "$BASE_DIR/voice_assistant.pid"

echo "Starting Plant Disease Model (Streamlit) on port 8501..."
cd "$BASE_DIR/plantDiease" && source .venv/bin/activate && streamlit run main.py --server.headless true --server.port 8501 > plant_disease.log 2>&1 &
echo $! > "$BASE_DIR/plant_disease.pid"

echo "Starting Crop Yield MVP (Streamlit) on port 8502..."
cd "$BASE_DIR/crop-yield/crop-yield-mvp" && source venv/bin/activate && streamlit run app.py --server.port 8502 > crop_yield.log 2>&1 &
echo $! > "$BASE_DIR/crop_yield.pid"

echo "Starting Smart Irrigation ML Server (Node) on port 5002..."
cd "$BASE_DIR/smart-irrigation-ml/backend" && npm install && node server.js > irrigation_ml.log 2>&1 &
echo $! > "$BASE_DIR/irrigation_ml.pid"

echo "Starting Weather Disaster Alert (Node) on port 5001..."
cd "$BASE_DIR/weather-disaster-alert" && npm install && node index.js > weather_alert.log 2>&1 &
echo $! > "$BASE_DIR/weather_alert.pid"

echo "Starting AgriSmart Frontend (React) on port 3000..."
cd "$BASE_DIR/agrismart" && npm install && npm start > frontend.log 2>&1 &
echo $! > "$BASE_DIR/frontend.pid"

echo "All services started! PIDs are saved in their respective .pid files in the root folder."

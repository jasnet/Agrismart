#!/bin/bash

BASE_DIR="/Applications/MCA PROJECT"

# Array of PID files
PID_FILES=("backend.pid" "smart-irrigation-backend.pid" "voice_assistant.pid" "plant_disease.pid" "crop_yield.pid" "irrigation_ml.pid" "weather_alert.pid" "frontend.pid")

for pid_file in "${PID_FILES[@]}"; do
    FILE_PATH="$BASE_DIR/$pid_file"
    if [ -f "$FILE_PATH" ]; then
        PID=$(cat "$FILE_PATH")
        echo "Killing process $PID from $pid_file..."
        kill -9 $PID 2>/dev/null
        rm "$FILE_PATH"
    else
        echo "No PID file found for $pid_file."
    fi
done

# Additional cleanup for dangling node/python/streamlit processes if necessary
echo "Attempting to clean up any remaining dangling processes mapped to our known ports..."
lsof -ti:8000,8001,5003,8501,8502,5002,5001,3000 | xargs kill -9 2>/dev/null

echo "All services stopped."

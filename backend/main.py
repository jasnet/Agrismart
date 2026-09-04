from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib, pandas as pd, os, sqlite3, json
from datetime import datetime
from pathlib import Path
from pymongo import MongoClient
import bcrypt

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "app.db"
MODEL_PATH = BASE_DIR / "models" / "fertility_model.joblib"

# ---------- MongoDB & Auth Setup ----------
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["agrismart"]
users_collection = mongo_db["users"]

def verify_password(plain_password, hashed_password):
    # bcrypt.checkpw requires bytes
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password, hashed_password)

def get_password_hash(password):
    # bcrypt.hashpw requires bytes
    if isinstance(password, str):
        password = password.encode('utf-8')
    # Generate salt and hash
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode('utf-8')  # Store as string for easy JSON transport


from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Soil Fertility API")

static_dir = BASE_DIR / "frontend"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Serve index.html at root
from fastapi.responses import FileResponse

@app.get("/")
async def read_index():
    index_file = BASE_DIR / "frontend" / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "AgriSmart Soil Fertility API is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Load Model ----------
if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)
else:
    model = None

FERTILIZER_MODEL_PATH = BASE_DIR / "models" / "fertilizer_model.joblib"
if FERTILIZER_MODEL_PATH.exists():
    fertilizer_model = joblib.load(FERTILIZER_MODEL_PATH)
    print("Fertilizer model loaded successfully.")
else:
    fertilizer_model = None
    print("Fertilizer model not found.")


# ---------- Input Model ----------
class SoilInput(BaseModel):
    N: float
    P: float
    K: float
    ph: float
    temperature: float
    humidity: float
    rainfall: float

class FertilizerInput(BaseModel):
    Temparature: float
    Humidity: float
    Moisture: float
    Nitrogen: float
    Potassium: float
    Phosphorous: float
    Soil_Type: str
    Crop_Type: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class SMSInput(BaseModel):
    message: str
    to: str = "+919876543210"

class WasteInput(BaseModel):
    wasteType: str
    quantity: str
    context: str
    location: str


# ---------- Initialize Database ----------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_json TEXT,
        result_json TEXT,
        created_at TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS crop_soil_profile (
        crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_name TEXT UNIQUE,
        nitrogen_req TEXT, phosphorus_req TEXT, potassium_req TEXT,
        pH_req TEXT, organic_carbon TEXT, rainfall_req TEXT, temperature_req TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS crop_types (
        type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_name TEXT,
        crop_type TEXT
    )""")
    conn.commit()
    conn.commit()
    conn.close()

init_db()

# ---------- Auth API ----------
@app.post("/auth/register")
def register_user_endpoint(user: UserRegister):
    # Check if user exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow().isoformat()
    }
    
    result = users_collection.insert_one(new_user)
    
    return {
        "message": "User created successfully",
        "user": {
            "name": user.name,
            "email": user.email,
            "id": str(result.inserted_id)
        }
    }

@app.post("/auth/login")
def login_user_endpoint(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    return {
        "message": "Login successful",
        "user": {
            "name": db_user["name"],
            "email": db_user["email"],
            "id": str(db_user["_id"])
        }
    }

# ---------- Prediction API ----------
@app.post("/predict")
def predict(data: SoilInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not found. Train it first.")

    df = pd.DataFrame([{
        "N": data.N,
        "P": data.P,
        "K": data.K,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "ph": data.ph,
        "rainfall": data.rainfall
    }])

    pred = model.predict(df)[0]
    result = {"fertility_or_crop": str(pred)}

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO predictions (input_json, result_json, created_at) VALUES (?,?,?)",
                (json.dumps(df.to_dict(orient='records')[0]),
                 json.dumps(result),
                 datetime.utcnow().isoformat()))
    pred_id = cur.lastrowid
    conn.commit()
    conn.close()

    result["prediction_id"] = pred_id
    result["recommended_crops"] = ["Rice", "Maize"]  # Placeholder
    return result


# ---------- Crop Info API ----------
@app.get("/crop-info/{crop_name}")
def crop_info(crop_name: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM crop_soil_profile WHERE LOWER(crop_name)=?", (crop_name.lower(),))
    row = cur.fetchone()
    cur.execute("SELECT crop_type FROM crop_types WHERE LOWER(crop_name)=?", (crop_name.lower(),))
    type_row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Crop not found")

    profile = {
        "crop_name": row[1],
        "nitrogen_req": row[2],
        "phosphorus_req": row[3],
        "potassium_req": row[4],
        "pH_req": row[5],
        "organic_carbon": row[6],
        "rainfall_req": row[7],
        "temperature_req": row[8]
    }
    crop_type = type_row[0] if type_row else None

    return {"profile": profile, "type": crop_type}


# ---------- Plant Disease API ----------
# import tensorflow as tf
from fastapi import File, UploadFile
import random
CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

import base64

@app.post("/predict-disease")
async def predict_disease(file: UploadFile = File(...)):
    try:
        # Read and encode image
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode('utf-8')
        
        # Prepare list for prompt
        classes_list = ", ".join(CLASS_NAMES)
        
        try:
            # Call OpenAI for analysis
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": f"""You are an agricultural expert AI. Analyze the image to detect crop diseases.
                        First, verify if the image contains a plant, leaf, or crop. 
                        - If the image is NOT a plant (e.g., a document, person, resume, random object), return strictly: {{"is_plant": false}}
                        - If it IS a plant, classify it into exactly one of these categories: {classes_list}.
                        
                        Return JSON format:
                        {{
                            "is_plant": true,
                            "crop": "Crop Name (e.g. Potato)",
                            "condition": "Condition (e.g. Early Blight or Healthy)",
                            "disease_name": "EXACT_CLASS_NAME_FROM_LIST",
                            "confidence": 0.95,
                            "description": "A brief 1-2 sentence description of this condition.",
                            "recommendations": [
                                "Actionable step 1",
                                "Actionable step 2"
                            ]
                        }}
                        """
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this crop image."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            if not result.get("is_plant", False):
                raise HTTPException(status_code=400, detail="Image does not appear to be a plant. Please upload a clear photo of a crop or leaf.")

            return {
                "crop": result.get("crop", "Unknown"),
                "condition": result.get("condition", "Unknown"),
                "disease": result.get("disease_name", "Unknown"),
                "description": result.get("description", ""),
                "recommendations": result.get("recommendations", []),
                "confidence": result.get("confidence", 0.85),
                "note": "AI Analysis by AgriSmart Vision"
            }

        except Exception as openai_error:
            print(f"OpenAI Error (Falling back to Mock): {openai_error}")
            # Fallback to Mock Logic on API Failure
            import random
            import time
            time.sleep(1.5) # Simulate analysis time
            
            # Simple randomness for demo purposes
            result_index = random.randint(0, len(CLASS_NAMES) - 1)
            raw_disease = CLASS_NAMES[result_index]
            confidence = random.uniform(0.88, 0.99)
            
            # Parse raw name for mock display
            parts = raw_disease.replace("___", " ").replace("_", " ").split(" ")
            crop = parts[0]
            condition = " ".join(parts[1:])
            
            return {
                "crop": crop,
                "condition": condition,
                "disease": raw_disease,
                "description": f"This appears to be {condition} affecting a {crop} plant. Regular monitoring is recommended.",
                "recommendations": [
                    "Isolate the affected plant if possible.",
                    "Apply appropriate treatment based on local agricultural guidelines."
                ],
                "confidence": confidence,
                "note": "Demo Mode (AI Service Quota Exceeded)"
            }

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Disease Prediction Error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/predict-fertilizer")
def predict_fertilizer(data: FertilizerInput):
    print(f"Received fertilizer prediction request: {data}")
    if not fertilizer_model:
        print("Error: Fertilizer model not loaded")
        return {"error": "Fertilizer model not loaded"}
    
    try:
        # Create DataFrame from input
        input_data = pd.DataFrame([{
            "Temparature": data.Temparature,
            "Humidity": data.Humidity,
            "Moisture": data.Moisture,
            "Nitrogen": data.Nitrogen,
            "Potassium": data.Potassium,
            "Phosphorous": data.Phosphorous,
            "Soil Type": data.Soil_Type,
            "Crop Type": data.Crop_Type
        }])
        print(f"Input DataFrame:\n{input_data}")
        
        prediction = fertilizer_model.predict(input_data)[0]
        print(f"Prediction result: {prediction}")
        
        # Map to user-friendly names
        name_mapping = {
            "14-35-14": "NPK 14-35-14",
            "20-20": "NPK 20-20",
            "28-28": "NPK 28-28",
            "10-26-26": "NPK 10-26-26",
            "17-17-17": "NPK 17-17-17"
        }
        
        formatted_prediction = name_mapping.get(prediction, prediction)
        
        return {"recommended_fertilizer": formatted_prediction}
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"error": str(e)}


# ---------- SMS API (Simulation) ----------
@app.post("/send-sms")
def send_sms_endpoint(data: SMSInput):
    # Log to server console to simulate sending
    print(f"------------ SMS SERVICE ------------")
    print(f"To: {data.to}")
    print(f"Message: {data.message}")
    print(f"Status: Sent via Simulation Gateway")
    print(f"-------------------------------------")
    
    # In a real app, you would use Twilio here:
    # client.messages.create(body=data.message, from_=TWILIO_PHONE, to=data.to)
    
    return {"status": "success", "message": "SMS sent successfully"}

# ---------- Chatbot API ----------
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env from backend folder
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

# Temporary debug - safe to show in logs
print("DEBUG: OPENAI_API_KEY present?:", bool(os.getenv("OPENAI_API_KEY")))
print("DEBUG: GEMINI_API_KEY present?:", bool(os.getenv("GEMINI_API_KEY")))
print("DEBUG: OPENAI_ORG_ID value:", os.getenv("OPENAI_ORG_ID"))
print("DEBUG: OPENAI_PROJECT_ID value:", os.getenv("OPENAI_PROJECT_ID"))

client_kwargs = {"api_key": os.getenv("OPENAI_API_KEY")}
org = os.getenv("OPENAI_ORG_ID")
proj = os.getenv("OPENAI_PROJECT_ID")

if org:
    client_kwargs["organization"] = org
if proj:
    client_kwargs["project"] = proj

client = OpenAI(**client_kwargs)

# Initialize Gemini
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    genai.configure(api_key=gemini_key)
    # Using 'gemini-2.0-flash' as primary, with fallback logical inside endpoint if needed
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    gemini_model = None

class ChatInput(BaseModel):
    message: str
    system_prompt: str

@app.post("/chat")
async def chat_endpoint(data: ChatInput):
    # 1. Try Gemini
    if gemini_key:
        models_to_try = [
            'models/gemini-2.1-flash-lite',
            'models/gemini-flash-lite-latest',
            'models/gemini-2.5-flash-lite',
            'models/gemini-2.5-flash',
            'models/gemini-2.0-flash',
            'models/gemma-3-27b-it',
            'models/gemma-3-12b-it',
            'models/gemma-3-4b-it'
        ]
        for model_name in models_to_try:
            try:
                temp_model = genai.GenerativeModel(model_name)
                full_prompt = f"{data.system_prompt}\n\nUser: {data.message}"
                response = temp_model.generate_content(full_prompt)
                return {"response": response.text}
            except Exception as e:
                print(f"Gemini {model_name} Error: {e}")
                continue

    # 2. Try OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": data.system_prompt},
                {"role": "user", "content": data.message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        
    # 3. Fallback to apology
    return {"response": "I'm sorry, I'm having trouble connecting to the AI brain. Please check your internet or API key."}

# ---------- Crop Yield API ----------
class YieldPredictionInput(BaseModel):
    ndvi: float
    nitrogen: float
    ph: float

@app.post("/predict-yield")
def predict_yield(data: YieldPredictionInput):
    try:
        try:
            project_root = BASE_DIR.parent
            mvp_dir = project_root / "crop-yield" / "crop-yield-mvp"
            model_path = mvp_dir / "outputs" / "model.joblib"
            
            if not model_path.exists():
                 raise Exception("Model file missing")
                 
            bundle = joblib.load(model_path)
            model = bundle['model']
            
            # Heuristics for derived fields
            ndvi_mean = data.ndvi
            ndvi_max = min(ndvi_mean * 1.2, 1.0)
            ndvi_auc = ndvi_mean * 120 
            
            input_df = pd.DataFrame([{
                'ndvi_mean_season': ndvi_mean,
                'ndvi_max_season': ndvi_max,
                'ndvi_auc_approx': ndvi_auc,
                'soil_ph': data.ph,
                'nitrogen_applied_kg_ha': data.nitrogen
            }])
            
            pred = model.predict(input_df)[0]
            return {"predicted_yield": round(pred, 2)}
        
        except Exception as model_err:
            print(f"Model Inference Failed (Using Heuristic): {model_err}")
            # Heuristic Calculation
            # Base 3T + NDVI contribution + Nitrogen boost - pH penalty
            heuristic_yield = 3.0 + (data.ndvi * 5.0) + (data.nitrogen * 0.025) - (abs(data.ph - 6.5) * 0.5)
            return {"predicted_yield": round(max(heuristic_yield, 0.5), 2)}
        
    except Exception as e:
        print(f"Yield Prediction Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/yield-data")
def get_yield_data():
    try:
        # Define paths
        project_root = BASE_DIR.parent
        mvp_dir = project_root / "crop-yield" / "crop-yield-mvp"
        
        model_path = mvp_dir / "outputs" / "model.joblib"
        ndvi_path = mvp_dir / "outputs" / "ndvi_zonal_stats.csv"
        soil_path = mvp_dir / "data" / "soil_and_ops.csv"
        fields_path = mvp_dir / "data" / "fields.geojson"
        
        if not model_path.exists():
            return {"error": "Model not found"}
            
        # Load data
        model_bundle = joblib.load(model_path)
        model = model_bundle['model']
        features = model_bundle['features']
        
        ndvi_df = pd.read_csv(ndvi_path)
        soil_df = pd.read_csv(soil_path)
        
        # Load fields to get crop type
        with open(fields_path, 'r') as f:
            geojson = json.load(f)
        
        field_props = []
        for feature in geojson['features']:
            props = feature['properties']
            field_props.append(props)
        fields_df = pd.DataFrame(field_props)
        
        # Merge
        # Start with fields
        merged = fields_df.merge(ndvi_df, on='field_id', how='left')
        merged = merged.merge(soil_df, on='field_id', how='left')
        merged = merged.fillna(0)
        
        # Predict
        X = merged[features]
        merged['pred_yield'] = model.predict(X)
        
        # Construct GeoJSON response
        features_list = []
        for i, row in merged.iterrows():
            # Find original feature for geometry
            orig_feature = geojson['features'][i] # Assuming order is preserved
            
            crop = row.get('crop_type', 'Unknown')
            yield_val = round(row['pred_yield'], 2)
            
            # Map emoji
            emoji = "🌱"
            if "corn" in crop.lower(): emoji = "🌽"
            elif "wheat" in crop.lower(): emoji = "🌾"
            elif "soy" in crop.lower(): emoji = "🫘"
            
            properties = {
                "field_id": row['field_id'],
                "crop_type": crop,
                "pred_yield": yield_val,
                "ndvi": round(row.get('ndvi_mean_season', 0), 2),
                "soil_ph": round(row.get('soil_ph', 0), 1),
                "nitrogen": int(row.get('nitrogen_applied_kg_ha', 0)),
                "emoji": emoji,
                "emojiColor": "#ffd54f" if "corn" in crop.lower() else "#81c784"
            }
            
            features_list.append({
                "type": "Feature",
                "geometry": orig_feature['geometry'],
                "properties": properties
            })
            
        return {
            "type": "FeatureCollection",
            "features": features_list,
            "stats": {
                "total_yield": round(merged['pred_yield'].sum(), 1),
                "avg_yield": round(merged['pred_yield'].mean(), 1),
                "avg_ndvi": round(merged['ndvi_mean_season'].mean(), 2),
                "field_count": len(merged)
            }
        }
        
    except Exception as e:
        print(f"Yield API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-waste")
async def predict_waste(data: WasteInput):
    prompt = f"""
    You are an expert waste management and circular economy AI named 'AgriSmart Waste-to-Resource'.
    Analyze the following waste profile and provide 2-3 specific, actionable, eco-friendly recommendations.
    
    Waste Type: {data.wasteType}
    Quantity: {data.quantity} kg/day
    Context: {data.context} (e.g., home, farm, restaurant)
    Location: {data.location} (e.g., urban, rural)
    
    Return the response strictly in this JSON format:
    {{
      "recs": [
        {{
          "method": "Name of Method",
          "desc": "Short description of the process",
          "reuse_location": "Where to implement (e.g., Backyard, Kitchen)",
          "product": "What is the final resource produced (e.g., Compost, Biogas)",
          "steps": ["Step 1", "Step 2", "Step 3"]
        }}
      ],
      "warnings": ["Warning 1", "Warning 2"]
    }}
    """
    
    # 1. Try Gemini
    if gemini_key:
        models_to_try = [
            'models/gemini-2.5-flash-lite',
            'models/gemini-flash-lite-latest',
            'models/gemini-2.5-flash',
            'models/gemini-2.0-flash',
            'models/gemma-3-27b-it',
            'models/gemma-3-12b-it',
            'models/gemma-3-4b-it'
        ]
        for model_name in models_to_try:
            try:
                temp_model = genai.GenerativeModel(model_name)
                response = temp_model.generate_content(prompt)
                text = response.text
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].strip()
                result = json.loads(text)
                
                # Use clean method names without "Gemini" branding
                for rec in result.get("recs", []):
                    rec["method"] = f"🌟 {rec['method']}"
                
                return result
            except Exception as e:
                print(f"Gemini {model_name} Waste Error: {e}")
                continue

    # 2. Try OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"OpenAI Waste Error: {e}")

    # 3. Final Fallback (Simplified)
    return {
        "recs": [{
            "method": "General Composting",
            "desc": "Convert organic waste into nutrient-rich soil.",
            "reuse_location": "Garden",
            "product": "Compost",
            "steps": ["Collect waste", "Add to bin", "Wait for decomposition"]
        }],
        "warnings": ["Ensure proper aeration to avoid odors."]
    }

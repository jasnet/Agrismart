from flask import Flask, request, jsonify
from flask_cors import CORS
from agriculture_data import AGRI_KNOWLEDGE
import os
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

# Load key from main backend env or local env
# Check typical locations for .env
possible_env_paths = [
    os.path.join(os.path.dirname(__file__), ".env"),
    os.path.join(os.path.dirname(__file__), "../../backend/.env") 
]
for path in possible_env_paths:
    if os.path.exists(path):
        load_dotenv(path)
        print(f"Loaded .env from {path}")
        break

app = Flask(__name__)
CORS(app)

# Initialize OpenAI
api_key = os.getenv("OPENAI_API_KEY")
print(f"OpenAI Key Found: {bool(api_key)}")
client = OpenAI(api_key=api_key) if api_key else None

# Initialize Gemini
gemini_key = os.getenv("GEMINI_API_KEY")
print(f"Gemini Key Found: {bool(gemini_key)}")
if gemini_key:
    genai.configure(api_key=gemini_key)
    # Using 'gemini-2.0-flash' as it is available and fast
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    gemini_model = None

def get_gemini_response(query):
    # Prioritizing Lite models which are working in this environment
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
            response = temp_model.generate_content(
                f"You are an expert agricultural assistant named AgriSmart. Answer this question for a farmer in a clear, step-by-step format. Use bullet points or numbered lists where possible: {query}"
            )
            return response.text.strip()
        except Exception as e:
            print(f"Gemini {model_name} Error: {e}")
            continue # Try next model
            
    return None



def get_openai_response(query):
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[

                {"role": "system", "content": "You are an expert agricultural assistant named AgriSmart. Provide helpful, concise advice to farmers about crops, diseases, soil, and fertilizers in simple language. Always prioritize step-by-step instructions and bullet points. If the user asks about something unrelated to agriculture, politely steer them back or answer briefly."},
                {"role": "user", "content": query}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return f"AI Error: {str(e)}"

def generate_mock_response(query):
    """Generates a plausible-sounding response when AI is offline/quota exceeded."""
    query = query.lower()
    
    # Generic templates
    if "water" in query or "irrigation" in query:
        return "Water management is crucial. Most crops generally need 2-3cm of water per week, adjusting for rainfall. Ensure good drainage to prevent root rot."
    if "sun" in query or "light" in query:
        return "Most vegetable and grain crops require 6-8 hours of direct sunlight daily for optimal growth and yield."
    if "pest" in query or "insect" in query:
        return "Integrated Pest Management (IPM) is recommended. Start with neem oil sprays or sticky traps before moving to chemical pesticides."
    if "fertilizer" in query or "nutrient" in query:
        return "A balanced NPK fertilizer is usually best. Soil testing is recommended to determine exact nutrient needs."
    if "weed" in query:
        return "Weeding should be done regularly, especially in the early growth stages. Mulching can also help suppress weed growth."
    if "profit" in query or "money" in query:
        return "High-value crops like herbs, exotic vegetables, or cash crops typically offer better margins, but require more precise care and market access."
        
    if "soil" in query:
        return "Soil health is key. Regular testing for pH and nutrients (N-P-K) is recommended. Adding organic matter like compost improves structure for all soil types."
    if "disease" in query or "fungus" in query:
        return "Disease prevention starts with crop rotation and using resistant varieties. If symptoms appear, remove infected parts immediately and consult an expert for specific fungicide application."
    if "yield" in query or "increase" in query:
        return "To increase yield: ensure optimal spacing, timely irrigation, correct fertilizer dosage, and weed control. Hybrid seeds can also offer higher potential output."
        
    return "I am currently operating in offline mode. For specific crop advice, please ask about 'Wheat', 'Rice', 'Cotton', 'Maize', 'Sugarcane', 'Tomato', or 'Potato'. For general farming tips, ask about Water, Sun, or Soil."

def agriculture_answer(query):
    # 1. Try Gemini (Priority as per user request)
    gemini_response = get_gemini_response(query)
    if gemini_response and not gemini_response.startswith("Gemini Error:"):
        return gemini_response
        
    ai_error = gemini_response or ""

    # 2. Try OpenAI (Secondary)
    openai_response = get_openai_response(query)
    if openai_response and not openai_response.startswith("AI Error:"):
         return openai_response

    if openai_response:
        ai_error += f" | {openai_response}"

    # 3. Fallback to Local Knowledge Base
    print("Fallback to local knowledge...")
    query = query.lower()

    for crop, info in AGRI_KNOWLEDGE.items():
        if crop in query:
            if "grow" in query or "how to" in query or "kaise" in query:
                return info.get("grow","No info available")
            if "soil" in query or "mitti" in query:
                return info.get("soil","No soil info")
            if "fertilizer" in query or "khad" in query:
                return info.get("fertilizer","No fertilizer info")
            if "disease" in query or "rog" in query:
                return info.get("disease","No disease info")
            if "organic" in query or "jaivik" in query:
                return info.get("organic","No organic info")
            
            # Default fallback if only crop name is mentioned
            return f"Found info for {crop}: {info.get('grow')} Soil: {info.get('soil')}"

    if "black soil" in query or "kaali mitti" in query:
        return AGRI_KNOWLEDGE["black_soil"]["grow"]

    if "yellow leaves" in query or "peele patte" in query:
        return AGRI_KNOWLEDGE["yellow_leaves"]["treatment"]

    # 3. Final Fallback: Removed mock to ensure user gets API response
    print("AI could not generate a response. Please check API quota.")
    return "I'm sorry, I'm having trouble connecting to my AI core right now. Please try again in 1 minute or check your API key."

@app.route("/ask", methods=["POST"])
def ask():
    user_text = request.json.get("query","")
    response = agriculture_answer(user_text)
    return jsonify({"answer": response})

@app.route("/")
def home():
    return {"status":"Agri Assistant Backend Running (Gemini + OpenAI)"}

if __name__ == "__main__":
    app.run(debug=True, port=5003)

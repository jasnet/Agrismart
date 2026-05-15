import speech_recognition as sr
import pyttsx3
import json
import queue
import sounddevice as sd
import sys
import os
from vosk import Model, KaldiRecognizer
from agri_data import SOIL_DATA, DISEASE_DATA, AGRICULTURE_KNOWLEDGE

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

class AgriAssistant:
    def __init__(self):
        self.language = "english" # Default
        self.vosk_model_path = "models/vosk-hindi"
        
        # Initialize English Recognizer
        self.sr_recognizer = sr.Recognizer()
        
        # Initialize Hindi Model
        if os.path.exists(self.vosk_model_path):
            print("Loading Hindi Model...")
            self.vosk_model = Model(self.vosk_model_path)
            self.vosk_rec = KaldiRecognizer(self.vosk_model, 16000)
        else:
            print("Warning: Hindi model not found. Hindi mode disabled.")
            self.vosk_model = None

        self.audio_queue = queue.Queue()

    def vosk_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.audio_queue.put(bytes(indata))

    def listen_english(self):
        with sr.Microphone() as source:
            print("\n[English Mode] Listening...")
            self.sr_recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.sr_recognizer.listen(source, timeout=5)
                command = self.sr_recognizer.recognize_google(audio)
                print(f"You said: {command}")
                return command.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                print(f"Error: {e}")
                return ""

    def listen_hindi(self):
        if not self.vosk_model:
            speak("Hindi model missing.")
            self.language = "english"
            return ""

        print("\n[Hindi Mode] Listening (Say something)...")
        # Use a fresh stream for one command cycle
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self.vosk_callback):
            while True:
                data = self.audio_queue.get()
                if self.vosk_rec.AcceptWaveform(data):
                    result = json.loads(self.vosk_rec.Result())
                    text = result.get("text", "")
                    if text:
                        print(f"You said: {text}")
                        return text
    
    # --- Logic for Specific Features ---
    def process_soil_query(self, command):
        dataset = SOIL_DATA[self.language]
        found = False
        for key in dataset:
            if key in command:
                speak(dataset[key])
                found = True
                break
        if not found:
             # Fallback to general agriculture logic if specific key not found
             self.process_general_agriculture_hindi(command)

    def process_disease_query(self, command):
        dataset = DISEASE_DATA[self.language]
        found = False
        for key in dataset:
            if key in command:
                speak(dataset[key])
                found = True
                break
        if not found:
             self.process_general_agriculture_hindi(command)

    def process_general_agriculture_hindi(self, text):
        """New robust Hindi agriculture logic"""
        found_crop = False
        
        # 1. Check for specific Crop/Entity match in AGRICULTURE_KNOWLEDGE
        for crop, info in AGRICULTURE_KNOWLEDGE.items():
            if crop in text:
                found_crop = True
                if "उग" in text or "कैसे" in text or "विधि" in text:
                    speak(info.get("grow", "इसकी उगाने की जानकारी उपलब्ध नहीं है"))
                    return
                if "मिट्टी" in text or "soil" in text:
                    speak(info.get("soil", "इस फसल के लिए मिट्टी की जानकारी उपलब्ध नहीं है"))
                    return
                if "खाद" in text or "fertilizer" in text:
                    speak(info.get("fertilizer", "खाद की जानकारी उपलब्ध नहीं है"))
                    return
                if "पानी" in text or "सिंचाई" in text:
                    speak(info.get("irrigation", "सिंचाई जानकारी उपलब्ध नहीं है"))
                    return
                # Default if crop named but question unclear
                speak(f"{crop} के बारे में क्या जानना है? मिट्टी, खाद, या सिंचाई?")
                return

        # 2. Check for Organic/General terms if no specific crop matched
        if "जैविक" in text or "organic" in text:
            # Look for organic info in knowledge base
            if "organic" in AGRICULTURE_KNOWLEDGE:
                 speak(AGRICULTURE_KNOWLEDGE["organic"]["fertilizer"])
                 return
        
        # 3. Final Fallback
        speak("कृपया फसल का नाम और प्रश्न स्पष्ट बोलें। जैसे कि 'गेहूं के लिए खाद' या 'धान की सिंचाई'।")

    def run(self):
        speak("Agriculture Assistant Started. Default language is English.")
        
        while True:
            command = ""
            
            # 1. Listen based on current language
            if self.language == "english":
                command = self.listen_english()
            else:
                command = self.listen_hindi()

            if not command:
                continue

            # 2. Global Switching Commands
            if "hindi" in command and ("switch" in command or "bol" in command or "speak" in command):
                self.language = "hindi"
                speak("नमस्ते। अब मैं हिंदी में बात करूँगा।")
                continue
            
            if ("english" in command or "अंग्रेजी" in command) and ("switch" in command or "speak" in command or "talk" in command):
                self.language = "english"
                speak("Okay. Switched to English.")
                continue

            if "stop" in command or "exit" in command or "बंद" in command:
                speak("Goodbye. Happy Farming.")
                break

            # 3. Process Domain Commands
            
            # --- ENGLISH ---
            if self.language == "english":
                if "soil" in command:
                    self.process_soil_query(command)
                elif "disease" in command or "symptom" in command or "leaves" in command or "spots" in command or "powder" in command:
                    self.process_disease_query(command)
                elif "crop" in command and "advice" in command:
                    if "wheat" in command: speak("Wheat needs cool weather.")
                    elif "rice" in command: speak("Rice needs plenty of water.")
                    else: speak("Please specify the crop name.")
                else:
                    speak("I can help with Soil types and Crop diseases. Or say 'Switch to Hindi'.")

            # --- HINDI ---
            else:
                # Use the new robust logic for everything in Hindi
                self.process_general_agriculture_hindi(command)

if __name__ == "__main__":
    try:
        app = AgriAssistant()
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")

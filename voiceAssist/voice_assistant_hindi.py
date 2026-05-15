import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import pyttsx3
import sys

engine = pyttsx3.init()
engine.setProperty("rate", 145)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Path to the model
model = Model("models/vosk-hindi")
rec = KaldiRecognizer(model, 16000)

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def crop_advice(command):
    if "गेहूं" in command:
        speak("गेहूं ठंडे मौसम और दोमट मिट्टी में अच्छा उगता है")
    elif "धान" in command or "चावल" in command:
        speak("धान को अधिक पानी और गर्म मौसम की आवश्यकता होती है")
    elif "कपास" in command:
        speak("कपास काली मिट्टी और सूखे मौसम में अच्छी होती है")
    else:
        speak("इस फसल की जानकारी उपलब्ध नहीं है")

def main():
    speak("नमस्ते किसान मित्र। मैं आपका कृषि सहायक हूँ")

    # Open microphone stream
    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000,
                               dtype="int16", channels=1, callback=callback):
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text:
                        print("You said:", text)

                    if "फसल" in text:
                        crop_advice(text)
                    elif "बंद" in text or "रुको" in text:
                        speak("धन्यवाद। शुभ खेती।")
                        break
    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

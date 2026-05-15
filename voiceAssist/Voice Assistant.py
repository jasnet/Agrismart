import speech_recognition as sr
import pyttsx3
import datetime

engine = pyttsx3.init()
engine.setProperty('rate', 155)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        return ""

def crop_advice(crop):
    advice = {
        "wheat": "Wheat grows well in cool climate and loamy soil.",
        "rice": "Rice needs standing water and warm temperature.",
        "cotton": "Cotton grows best in black soil and warm climate.",
        "maize": "Maize requires moderate water and well drained soil."
    }
    speak(advice.get(crop, "Sorry, I do not have advice for this crop."))

def market_price(crop):
    prices = {
        "wheat": "Wheat price is approximately 2200 rupees per quintal.",
        "rice": "Rice price is approximately 3000 rupees per quintal.",
        "cotton": "Cotton price is approximately 7000 rupees per quintal."
    }
    speak(prices.get(crop, "Market price data not available."))

def assistant():
    speak("Hello. I am your free agriculture voice assistant.")
    speak("How can I help you today?")

    while True:
        command = listen()

        if "crop advice" in command or "crop" in command:
            speak("Please tell the crop name")
            crop = listen()
            crop_advice(crop)

        elif "market price" in command:
            speak("Tell me the crop name")
            crop = listen()
            market_price(crop)

        elif "time" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Current time is {time}")

        elif "date" in command:
            date = datetime.datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {date}")

        elif "stop" in command or "exit" in command:
            speak("Thank you. Happy farming.")
            break

assistant()

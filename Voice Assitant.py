import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import sys
import time
import random

# ─────────────────────────────────────────────
#  ENGINE SETUP
# ─────────────────────────────────────────────

engine = pyttsx3.init()

def set_voice():
    """Pick a clear English voice if available."""
    voices = engine.getProperty('voices')
    for v in voices:
        if 'english' in v.name.lower() or 'en' in v.id.lower():
            engine.setProperty('voice', v.id)
            break
    engine.setProperty('rate', 170)      # speaking speed
    engine.setProperty('volume', 1.0)    # max volume

set_voice()

# ─────────────────────────────────────────────
#  SPEAK & LISTEN
# ─────────────────────────────────────────────

def speak(text: str):
    """Convert text to speech."""
    print(f"\n  🤖 Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen() -> str:
    """Listen from microphone and return recognized text."""
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.0   # seconds of silence before stopping
    recognizer.energy_threshold = 300  # mic sensitivity

    with sr.Microphone() as source:
        print("\n  🎙️  Listening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print(f"  🧑 You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Sorry, I couldn't reach the speech service. Check your internet.")
        return ""

# ─────────────────────────────────────────────
#  COMMANDS
# ─────────────────────────────────────────────

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}."

def get_date():
    today = datetime.date.today()
    return f"Today is {today.strftime('%A, %B %d, %Y')}."

def open_website(command: str):
    sites = {
        "youtube"  : "https://youtube.com",
        "google"   : "https://google.com",
        "github"   : "https://github.com",
        "facebook" : "https://facebook.com",
        "instagram": "https://instagram.com",
        "twitter"  : "https://twitter.com",
        "wikipedia": "https://wikipedia.org",
        "gmail"    : "https://mail.google.com",
        "maps"     : "https://maps.google.com",
        "amazon"   : "https://amazon.in",
    }
    for name, url in sites.items():
        if name in command:
            webbrowser.open(url)
            return f"Opening {name.capitalize()} for you!"
    return None

def search_google(command: str):
    query = command.replace("search", "").replace("google", "").strip()
    if query:
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return f"Searching Google for: {query}"
    return "What do you want me to search?"

def tell_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the developer go broke? Because they used up all their cache!",
        "There are 10 types of people in the world — those who understand binary and those who don't.",
        "A SQL query walks into a bar, walks up to two tables and asks... Can I join you?",
        "Why do Java developers wear glasses? Because they don't C sharp!",
    ]
    return random.choice(jokes)

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

def calculate(command: str):
    """Simple safe calculator."""
    try:
        expr = command
        for word in ["calculate", "what is", "what's", "compute", "equals"]:
            expr = expr.replace(word, "")
        expr = expr.strip()
        expr = expr.replace("plus", "+").replace("minus", "-") \
                   .replace("times", "*").replace("multiplied by", "*") \
                   .replace("divided by", "/").replace("x", "*")
        allowed = set("0123456789+-*/(). ")
        if all(c in allowed for c in expr):
            result = eval(expr)
            return f"The answer is {result}"
        return "I couldn't compute that safely."
    except Exception:
        return "Sorry, I couldn't calculate that."

# ─────────────────────────────────────────────
#  COMMAND ROUTER
# ─────────────────────────────────────────────

def process_command(command: str) -> bool:
    """
    Process the command. Returns False to exit, True to continue.
    """
    if not command:
        speak("I didn't catch that. Could you repeat?")
        return True

    # Exit
    if any(w in command for w in ["exit", "quit", "bye", "goodbye", "stop", "shut down"]):
        speak("Goodbye da! Have a great day!")
        return False

    # Time & Date
    if "time" in command:
        speak(get_time())

    elif "date" in command or "today" in command:
        speak(get_date())

    # Greetings
    elif any(w in command for w in ["hello", "hi", "hey", "wassup", "what's up"]):
        speak(f"{get_greeting()}! I'm your voice assistant. How can I help you?")

    # How are you
    elif "how are you" in command:
        speak("I'm doing great, thanks for asking! Ready to help you da!")

    # Joke
    elif "joke" in command:
        speak(tell_joke())

    # Open website
    elif "open" in command:
        result = open_website(command)
        speak(result if result else "I'm not sure which website to open.")

    # Google search
    elif "search" in command or ("google" in command and "open" not in command):
        speak(search_google(command))

    # Calculate
    elif any(w in command for w in ["calculate", "what is", "compute", "how much is"]):
        speak(calculate(command))

    # Your name
    elif "your name" in command or "who are you" in command:
        speak("I'm your Python voice assistant! You can call me Jarvis.")

    # Weather placeholder
    elif "weather" in command:
        speak("I don't have live weather right now, but you can ask me to open Google Maps or search for your city's weather!")

    # Help
    elif "help" in command or "what can you do" in command:
        speak(
            "I can tell you the time and date, open websites like YouTube and Google, "
            "search Google, do math, tell jokes, and have a conversation. Just say the word!"
        )

    # Unknown
    else:
        responses = [
            "I'm not sure about that. Try asking something else!",
            "Hmm, I didn't get that. Want me to search Google for it?",
            "I don't know that one yet. I'm still learning!",
        ]
        speak(random.choice(responses))

    return True

# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────

WAKE_WORDS = ["hey assistant", "jarvis", "hello assistant", "ok assistant"]

def main():
    print("=" * 50)
    print("       🎙️  Python Voice Assistant")
    print("=" * 50)
    print("  Wake words : 'Jarvis' or 'Hey Assistant'")
    print("  Say 'exit' or 'bye' to quit")
    print("=" * 50)

    greeting = get_greeting()
    speak(f"{greeting}! Say 'Jarvis' or 'Hey Assistant' to wake me up.")

    while True:
        # Listen for wake word
        wake = listen()
        if not wake:
            continue

        # Check wake word
        if any(w in wake for w in WAKE_WORDS):
            speak("Yes? I'm listening!")
            time.sleep(0.3)

            # Listen for actual command
            command = listen()
            should_continue = process_command(command)
            if not should_continue:
                break

        # Direct command without wake word (for testing)
        elif any(w in wake for w in ["exit", "quit", "bye", "goodbye"]):
            speak("Goodbye da! Take care!")
            break

if __name__ == "__main__":
    main()
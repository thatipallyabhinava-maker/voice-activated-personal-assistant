import speech_recognition as sr
import pyttsx3
import requests
import feedparser
import time
from datetime import datetime, timedelta


# ---------------- TEXT TO SPEECH ----------------

engine = pyttsx3.init()


def speak(text):

    print("Assistant:", text)

    engine.say(text)

    engine.runAndWait()


# ---------------- VOICE INPUT ----------------

def listen():

    r = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            print("Listening...")

            r.adjust_for_ambient_noise(source, duration=1)

            audio = r.listen(source)

        text = r.recognize_google(audio)

        print("You:", text)

        return text.lower()

    except sr.UnknownValueError:

        speak("Sorry, I did not understand.")

        return ""

    except sr.RequestError:

        speak("Sorry, there is a problem with the speech service.")

        return ""

    except:

        speak("Sorry, there is a problem with the microphone.")

        return ""


# ---------------- WEATHER ----------------

def get_weather(city):

    # Put your NEW OpenWeather API key here
    api_key = "50eb5fb3b54d2c0d101aa7d625fc7f86"

    # Correct weather API URL
    url = "https://api.openweathermap.org/data/2.5/weather"

    parameters = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:

        response = requests.get(url, params=parameters)

        data = response.json()

        if response.status_code == 200:

            temperature = data["main"]["temp"]

            weather = data["weather"][0]["description"]

            speak(
                "The temperature in "
                + city
                + " is "
                + str(temperature)
                + " degrees Celsius."
            )

            speak("The weather is " + weather)

        else:

            speak("Sorry, I could not find that city.")

    except:

        speak("Sorry, I could not connect to the weather service.")


# ---------------- NEWS ----------------

def get_news():

    url = "https://feeds.bbci.co.uk/news/rss.xml"

    try:

        news = feedparser.parse(url)

        speak("Here are the latest news headlines.")

        if len(news.entries) == 0:

            speak("Sorry, I could not get the news.")

            return

        for i in range(min(5, len(news.entries))):

            title = news.entries[i].title

            print(title)

            speak(title)

    except:

        speak("Sorry, I could not get the news.")


# ---------------- REMINDER ----------------

def set_reminder():

    speak("What should I remind you about?")

    message = listen()

    if message == "":

        speak("I could not understand the reminder.")

        return

    speak("At what time should I remind you?")

    speak("Please say the time like 6 30 PM.")

    reminder_time = listen()

    if reminder_time == "":

        return

    try:

        # Change 6:30 PM into 6 30 PM
        reminder_time = reminder_time.replace(":", " ")

        # Convert spoken time
        reminder_time = datetime.strptime(
            reminder_time,
            "%I %M %p"
        )

        current_time = datetime.now()

        # Create reminder time
        reminder = current_time.replace(
            hour=reminder_time.hour,
            minute=reminder_time.minute,
            second=0,
            microsecond=0
        )

        # If time has already passed,
        # set reminder for tomorrow
        if reminder <= current_time:

            reminder = reminder + timedelta(days=1)

            speak("That time has already passed today.")

            speak("I will remind you tomorrow.")

        speak(
            "Reminder set for "
            + reminder.strftime("%I:%M %p")
        )

        print(
            "Reminder time:",
            reminder.strftime("%d-%m-%Y %I:%M %p")
        )

        # Wait until reminder time
        while True:

            current_time = datetime.now()

            if current_time >= reminder:

                speak("Reminder: " + message)

                break

            time.sleep(5)

    except:

        speak("Sorry, I could not understand the time.")

        speak("Please say the time like 6 30 PM.")


# ---------------- MAIN ASSISTANT ----------------

def assistant():

    speak("Hello! I am your personal assistant.")

    speak(
        "You can ask me for weather, news, or a reminder."
    )

    while True:

        command = listen()

        # If nothing was understood
        if command == "":

            continue

        # Hello
        elif "hello" in command or "hi" in command:

            speak("Hello! How can I help you?")

        # Name
        elif "your name" in command or "who are you" in command:

            speak("My name is Assistant.")

        # Weather
        elif "weather" in command:

            speak("Which city do you want the weather for?")

            city = listen()

            if city != "":

                get_weather(city)

        # News
        elif "news" in command:

            get_news()

        # Reminder
        elif "reminder" in command or "remind me" in command:

            set_reminder()

        # Exit
        elif (
            "exit" in command
            or "stop" in command
            or "quit" in command
            or "goodbye" in command
        ):

            speak("Goodbye! Have a nice day.")

            break

        # Unknown command
        else:

            speak(
                "Sorry, I don't know that command."
            )

            speak(
                "You can say hello, weather, news, reminder, or exit."
            )


# ---------------- START PROGRAM ----------------

assistant()
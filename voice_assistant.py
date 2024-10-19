import random
import speech_recognition as sr
import pyttsx3
import time
from requests import get
import google.generativeai as genai
from dotenv import load_dotenv
import os
import sys
import cv2
import pyautogui as pg
import webbrowser
from googlesearch import search
import pywhatkit as kit
from datetime import datetime
import keyboard as k


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# print(sr.Microphone.list_microphone_names()[2])

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 133)
engine.setProperty("volume", 1)


# text to speech
def speak(audio):
    for i in audio:
        if i == "*" or i == "#" or i == "`":
            continue
        else:
            print(i, end="")
    try:
        engine.say(audio)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"System is quitting with an error message {e}")
        sys.exit()

    return


def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=2) as mic:
        print("\nAsk something...")
        recognizer.adjust_for_ambient_noise(mic, duration=0.8)
        texted_audio = recognizer.listen(mic)

        print("\nInterpreting...")
        text = recognizer.recognize_google(texted_audio)
    try:
        print(f"\nRecognised Word : {text}\n")
    except sr.UnknownValueError():
        recognizer = sr.Recognizer()
        return None

    return text


def get_response(question):
    if len(question) <= 11:
        response = model.generate_content(
            question,
            generation_config=genai.types.GenerationConfig(
                stop_sequences=["x"],
                max_output_tokens=20,
                temperature=0.1,
            ),
        )
    else:
        response = model.generate_content(question)

    try:
        return speak(response.text)
    except Exception as e:
        speak(f"Logging out with an error message {e}")
        sys.exit()


def news():
    api = "http://newsapi.org/v2/top-headlines?sources=the-verge&apiKey=eb8314105df7445c8d6694ffe6546d92"
    mainPage = get(api).json()
    articles = mainPage["articles"]

    for article in articles:
        speak(article["description"])
        print("\n")

    return


# self made function
def get_url(url):
    url = f"https://www.youtube.com/results?search_query={url}"
    count = 0
    cont = get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')

    for i in lst:
        count += 1
        if i == "WEB_PAGE_TYPE_WATCH":
            break
        if lst[count - 5] == "/results":
            raise Exception("No Video Found for this Topic!")

    views_count = lst[count - 19]
    time_stamp = lst[count - 29]
    unique_id = lst[count - 5]

    return {
        "video_url": f"https://www.youtube.com{unique_id}",
        "time": time_stamp,
        "views": views_count,
    }


def fetch_top_search(query, num_results=10):
    search_results = search(query, num_results=num_results)
    return search_results


if __name__ == "__main__":
    speak("Good Morning Karan! How may i help you, if you want to have something ask me, i am here to assist you")
    count = 0
    while True:
        myobj = datetime.now()

        data = speech_to_text().lower()

        if "news" in data:
            try:
                news()
            except Exception as e:
                print(f"Caused Server side error with message {e}")

        elif "exit" in data:
            sys.exit()

        elif "close browser" in data:
            os.system("taskkill /f /im chrome.exe")

        elif "change tab" in data:
            pg.keyDown("alt")
            pg.press("tab")
            time.sleep(0.4)
            pg.keyUp("alt")

        elif "open office" in data:
            apath = (
                "C:\\Users\\karan\\AppData\\Local\\Kingsoft\\WPS Office\\ksolaunch.exe"
            )
            os.startfile(apath)
            time.sleep(5)

        elif "close office" in data:
            os.system("taskkill /f /im wps.exe")
            time.sleep(2)

        elif "find" in data:
            try:
                queue = speech_to_text().lower()
                speak(f"Showing you top 10 web result on {queue}\n")
                res = fetch_top_search(queue)

                for idx, result in enumerate(res, 1):
                    print(f"{idx}. {result}")

                time.sleep(10)
            except Exception as e:
                print("Error can't able to fetch the links")

        elif "open notepad" in data:
            npath = "C:\\Windows\\System32\\Notepad.exe"
            os.startfile(npath)
            time.sleep(2)

        elif "close notepad" in data:
            speak("closing notepad")
            os.system("taskkill /f /im notepad.exe")
            time.sleep(2)

        elif "open command prompt" in data:
            os.system("start cmd")
            time.sleep(5)

        elif "close command prompt" in data:
            os.system("taskkill /f /im cmd.exe")
            time.sleep(5)

        elif "open camera" in data:
            try:
                cap = cv2.VideoCapture(0)
                frame = 0
                speak("Camera is going to open till 240 frames if you want more to access change the settings")
                while True:
                    ret, img = cap.read()
                    cv2.imshow("webcam", img)
                    frame += 1
                    if cv2.waitKey(1) & 0xFF == ord("q") or frame == 240:
                        frame = 0
                        break
                cap.release()
                cv2.destroyAllWindows()
            except Exception as e:
                print("Can't able to open camera")

        elif "battery percentage" in data:
            import psutil

            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f"We left with only {percentage}%")

        elif "choose a random number" in data:
            num = random.randint(0, 9)
            speak(num)

        elif "wait" in data:
            try:
                if count == 2:
                    print("Exiting the assistance")
                    sys.exit()
                else:
                    time.sleep(10)
                count += 1
            except Exception as e:
                print("Error not able to pause the system")

        elif "take a screenshot" in data:
            speak("Tell with what name should i save this screenshot")
            name = speech_to_text().lower()
            img = pg.screenshot()
            img.save(f"{name}.png")
            speak("Clicked..")

        elif "open web browser" in data:
            speak("What should i open")
            webApp = speech_to_text().lower()

            if "youtube" in webApp:
                webbrowser.open("youtube.com")
            elif "twitter" in webApp:
                webbrowser.open("twitter.com")
            elif "facebook" in webApp:
                webbrowser.open("facebook.com")
            elif "instagram" in webApp:
                webbrowser.open("instagram.com")
            elif "problem" in webApp:
                webbrowser.open("leetcode.com")
            elif "hackerrank" in webApp:
                webbrowser.open("hackerrank.com")
                break
            else:
                speak("What should I search on google\n")
                searchQuery = speech_to_text().lower()
                webbrowser.open(f"{searchQuery}")
            # time.sleep(10)

        elif "start youtube" in data:
            try:
                speak("What would you want to see on youtube")
                songName = speech_to_text().lower()
                video_url = get_url(songName)
                webbrowser.open(video_url['video_url'])
            except Exception as e:
                print("Can't able to open youtube check your connection or may be spell")
            sys.exit()

        elif "send message" in data:
            details = {"aman": "+918383802145"}
            hr = int(myobj.hour)
            min = int(myobj.minute)

            speak("Whom would you like to send the message")
            name = speech_to_text().lower()

            min += 2
            print(hr, min)
            speak("What would you like to send the message")

            try:
                message = speech_to_text().lower()
                kit.sendwhatmsg(details[name], message, hr, min, 26, True, 3)
            except Exception as e:
                print(f"Unable to send the message: {e}")
            time.sleep(10)

        else:
            try:
                get_response(data)
            except Exception as e:
                print(f"Unable to process the request with error message {e}")

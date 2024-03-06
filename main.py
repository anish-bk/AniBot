import speech_recognition as sr
import win32com.client as wincl
import requests
import webbrowser
import openai
from datetime import datetime
import subprocess
from playsound import playsound
import os

def weather(city):
    weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + weather_api_key
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    if api_data['cod'] == '404':
        say("Invalid City: {}, Please check your city name.".format(city))
        return False
    else:
        temp_city = ((api_data['main']['temp']) - 273.15)
        max_temp = ((api_data['main']['temp_max']) - 273.15)
        min_temp = ((api_data['main']['temp_min']) - 273.15)
        weather_desc = api_data['weather'][0]['description']
        hmdt = api_data['main']['humidity']
        wind_spd = api_data['wind']['speed']
        date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
        print("--------------------------------------------------------------")
        print("Weather Stats for - {}  || {}".format(city.upper(), date_time))
        print("--------------------------------------------------------------")
        print("Current temperature is: {:.2f} deg C".format(temp_city))
        print("Maximum temperature is: {:.2f} deg C".format(max_temp))
        print("Minimum temperature is: {:.2f} deg C".format(min_temp))
        print("Current weather desc  :", weather_desc)
        print("Current humidity      :", hmdt, '%')
        print("Current wind speed    :", wind_spd, 'kmph')
        say("The weather has been printed to the console.")
        return True

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"User: {query}\n AniBot: "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful personal assistant, capable of performing almost every task requested."},
                  {"role": "user", "content": query}]
    )
    # todo: wrap this inside of a try catch block
    say(response["choices"][0]["message"]["content"])
    chatStr += f"{response['choices'][0]['message']['content']}\n"
    return response["choices"][0]["message"]['content']

def news():
    news_api_key = os.getenv("NEWS_API_KEY")
    base_url = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=" + news_api_key
    response = requests.get(base_url).json()
    articles = response["articles"]
    result = []
    for ar in articles:
        result.append(ar["title"]+"\n"+ar["url"])
    for i in range(10):
        print(i+1,'] ',result[i])

def ai(prompt):
    text = f"OpenAI response for Prompt: {prompt} \n ***************************************\n\n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are the best programmer in the world. You can and you have to write program for every problem you are assigned."},
            {"role": "user", "content": prompt}
        ]
    )
    text += response["choices"][0]["message"]["content"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"D:\\Openai\\{''.join(prompt.split('intelligence')[1:]).strip()}", 'w') as f:
        f.write(text)

def say(text):
    speaker = wincl.Dispatch(("SAPI.SpVoice"))
    voices = speaker.GetVoices()
    speaker.Voice = voices.Item(1)
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-ne")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Are you listening?"

if __name__ == '__main__':
    print("It's AniBot! Let's get started! \n")
    say("Hello I am AniBot. How can be I of your service?")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"],
                 ["facebook", "https://facebook.com"],
                 ["instagram", "https://instagram.com"],
                 ["twitter", "https://twitter.com"],
                 ["linkedin", "https://linkedin.com"],
                 ["github", "https://github.com"],
                 ["stackoverflow", "https://stackoverflow.com"],
                 ["reddit", "https://reddit.com"],
                 ["pinterest", "https://pinterest.com"],
                 ["tiktok", "https://tiktok.com"],
                 ["netflix", "https://netflix.com"],
                 ["amazon", "https://amazon.com"],
                 ["yahoo", "https://yahoo.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}, Sir.")
                webbrowser.open(site[1])
        if "play music" in query:
            say("Playing your favourite song")
            playsound("C:\\Music\\music.mp3")
        elif "play song" in query:
            say("Playing your favourite song")
            playsound("C:\\Music\\song.mp3")
        elif "play video" in query:
            say("Playing video")
            webbrowser.open("https://www.youtube.com/watch?yourvideo")
        elif "the time" in query:
            strftime = datetime.now().strftime("%H:%M:%S")
            say(f"Sir the time is {strftime}")
        elif "open word pad".lower() in query.lower():
            app_path = "C:\\Program Files\\Windows NT\\Accessories\\wordpad.exe"
            subprocess.Popen(app_path)
        elif "open visual studio code".lower() in query.lower():
            app_path = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
            subprocess.Popen(app_path)
        elif "using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "weather".lower() in query.lower():
            say("Sure, what city do you want to know the weather of?")
            city = takeCommand()
            print("Fetching Weather Data...\n")
            weather(city)
        elif "news".lower() in query.lower():
            print("Getting latest news...\n")
            news()
            say("News has been printed to the console.")
        elif "exit".lower() in query.lower():
            say("Say password if you want to exit.")
            if "password".lower() in takeCommand().lower():
                say("Nice to have a chat with you. Bye.")
                exit()
            elif "no".lower() in takeCommand().lower():
                say("Ok Sir.")
        elif "clear chat".lower() in query.lower():
            chatStr = ""
            os.system("cls")
            say("Chat has been cleared.")
        else:
            print("Chatting...\n")
            response = chat(query)
            print(f"AniBot said: {response}")

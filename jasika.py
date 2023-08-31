import json
import os
import sys
from urllib.request import urlopen
import wolframalpha
import shutil
import pyjokes
import webbrowser
import wikipedia
import pyttsx3
import datetime
import speech_recognition as sr
import requests
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jasikaui1 import Ui_Form


engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18 :
        speak("Good Afternoon!") 

    else :
        speak("Good Evening!")
    assname = "JASIKA"
    speak(f"HI I am {assname}\n.")

def username():
    speak("what should i call you?")
    uname = takecommand()
    speak("welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns

    print("####################".center(columns))
    print("Welcome Mr .", uname.center(columns))
    print("####################".center(columns))
    speak("how can i help you")


def takecommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}\n")

    except Exception as e:
        speak("please Say that Again...")
        print("please say that Again...")
        return "None"
    return query
    

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        wishMe()
        username()

        while True:
                query= takecommand().lower()

                if 'wikipedia' in query:
                    speak("Searching Wikipedia...")
                    query= query.replace("wikipedia","")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia...")
                    print(results)
                    speak(results)



                elif 'open youtube' in query:
                    webbrowser.open("youtube.com")

                elif 'open google' in query:
                    webbrowser.open("google.com")

                elif 'open insta' in query:
                    webbrowser.open("instagram.com")

                elif 'play music' in query:
                    music_dir = 'D:\project\JASIKA\music'
                    songs = os.listdir(music_dir)
                    print (songs)
                    os.startfile(os.path.join(music_dir, songs[0]))
                

                elif 'open C drive ' in query:
                    os.startfile("C:")

                elif 'open d drive' in query:
                    os.startfile("D:")

                elif 'open e drive' in query:
                    os.startfile("E:")

                elif 'hello jessica' in query:
                    speak("Hello Sir...")
                    print("Hello Sir...")

                elif "how are you" in query:
                    speak("I'm fine, glad you asked me that")
                    print("I'm fine, glad you asked me that")

                elif "morning" in query or "afternoon" in query:
                    speak("A warm" +query)
                    speak("How are you ")
                    print("A warm" +query)
                    

                elif 'joke' in query:
                    speak(pyjokes.get_joke())
                    print(pyjokes.get_joke())


                elif 'search' in query or 'play' in query:
                    
                    query = query.replace("search", "")
                    query = query.replace("play", "")         
                    webbrowser.open(query)
                
                elif 'is love' in query:
                    speak("It is 7th sense that destroy all other senses")
                    print("It is 7th sense that destroy all other senses")
                
                elif "weather" in query:
                    api_key="566702c9ffbc32b2631435ad94ff06f4"
                    base_url="https://api.openweathermap.org/data/2.5/weather?"
                    speak("what is the city name")
                    city_name=takecommand()
                    complete_url=base_url+"appid="+api_key+"&q="+city_name
                    response = requests.get(complete_url)
                    x=response.json()
                    if x["cod"]!="404":
                        y =x["main"]
                        current_temperature = y["temp"]
                        current_humidiy = y["humidity"]
                        z = x["weather"]
                        weather_description = z[0]["description"]
                        speak(" Temperature in kelvin unit is " +
                            str(current_temperature) +
                            "\n humidity in percentage is " +
                            str(current_humidiy) +
                            "\n description  " +
                            str(weather_description))
                        print(" Temperature in kelvin unit = " +
                            str(current_temperature) +
                            "\n humidity (in percentage) = " +
                            str(current_humidiy) +
                            "\n description = " +
                            str(weather_description))

                elif 'the time' in query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")   
                    speak(f"Sir, the time is {strTime}")
                    print(f"Sir, the time is {strTime}")
                
                elif "calculate" in query:
                    
                    app_id = "KR9QE5-XT6ULT6VQ3"
                    client = wolframalpha.Client(app_id)
                    indx = query.lower().split().index('calculate')
                    query = query.split()[indx + 1:]
                    res = client.query(' '.join(query))
                    answer = next(res.results).text
                    print("The answer is " + answer)
                    speak("The answer is " + answer)

                elif "write a note" in query:
                    speak("What should i write, sir")
                    note = takecommand()
                    file = open('JASIKA.txt', 'w')
                    speak("Sir, Should i include date and time")
                    snfm = takecommand()
                    if 'yes' in snfm or 'sure' in snfm:
                        strTime = datetime.datetime.now().strftime("%H:%M:%S")
                        file.write(strTime)
                        file.write(" :- ")
                        file.write(note)
                    else:
                        file.write(note)

                elif "show note" in query:
                    speak("Showing Notes")
                    file = open("JASIKA.txt", "r")
                    print(file.read())
                    speak(file.read(6))

                elif 'news' in query:
                    
                    try:
                        jsonObj = urlopen("https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=de9b4d34207447f9a1275d294dc44f05")
                        data = json.load(jsonObj)
                        i = 1
                        
                        speak("here are some top news from the times of india")
                        print("=============== TIMES OF INDIA ============"+ '\n')
                        
                        for item in data['articles']:
                            
                            print(str(i) + '. ' + item['title'] + '\n')
                            print(item['description'] + '\n')
                            speak(str(i) + '. ' + item['title'] + '\n')
                            i += 1
                    except Exception as e:
                        
                        print(str(e))

                elif "what is" in query or "who is" in query:
                    
                    client = wolframalpha.Client("KR9QE5-XT6ULT6VQ3")
                    res = client.query(query)
                    
                    try:
                        print (next(res.results).text)
                        speak (next(res.results).text)
                    except StopIteration:
                        print ("No results")

                elif 'powerpoint presentation' in query:
                    speak("opening Power Point presentation")
                    power = "C:\\Users\\Devjp\\OneDrive\Desktop\\JASIKA\\Presentation\\J.A.S.I.K.A. (4).pptx"
                    os.startfile(power)

                elif 'excel' in query:
                    speak("Opening Excel....")
                    print("Opening Excel....")
                    Excel = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel.lnk"
                    os.startfile(Excel)

                elif 'word' in query:
                    speak("Opening Word...")
                    print("Opening Word...")
                    word = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk"
                    os.startfile(word)

                elif 'open epic games' in query:
                    speak("opening Epic Games Launcher...")
                    print("opening Epic Games Launcher...")
                    epic = "C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe"
                    os.startfile(epic)

            
    
startExecution = MainThread()


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton_2.clicked.connect(self.startTask)

    def __del__(self):
        sys.stdout = sys.__stdout__

    
    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:\\Users\\Devjp\\OneDrive\\Desktop\\JASIKA\\GUI\\jasika.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()



app = QApplication(sys.argv)
jasika = Main()
jasika.show()
exit(app.exec_())
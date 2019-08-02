from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import requests
import random
import pygame
from pygame import mixer
import time
from time import ctime
import forecastio
from chatterbot import ChatBot
#from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot("Jarvis")

wapi_key = "21a743f3dbcdac18426bef5c9262183b"
lat = 30.3534010
lng = 76.3692080


 
 
def say(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
       
    #  use the system's inbuilt say command instead of mpg123
       tts = gTTS(text=audio, lang='en')
       pygame.mixer.init(28000, -8,2,8000)
       mixer.music.load('blank.mp3')
       tts.save("audio.mp3")
       mixer.music.load('audio.mp3')
       mixer.music.play()



def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command

def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)
 
 
def analyze(statement):
    for pattern, responses in psychobabble:
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])



def assistant(command):
    "if statements for executing commands"

    if 'open' in command:

      if 'C drive' in command:
        os.startfile('C:\\') 
        say('Done!')

      if 'D drive' in command:
        os.startfile('D:\\') 
        say('Done!')
        
      if 'quora' in command:
        webbrowser.open('www.quora.com')
        say('Done!')

      if 'facebook' in command:
        webbrowser.open('www.facebook.com')
        say('Done!')


      if '.com' in command:
        sf=re.split('\\bopen \\b',command)[-1]
        f=sf.replace(' ','')
        greet='I have opened '+f
        say(greet)
        webbrowser.open('www.'+f)

    
       
        
      else:
        sf=re.split('\\bopen\\b',command)[-1]
        greet='I have opened '+sf
        say(greet)
        os.system('start'+ sf)
        


    elif 'quit' in command:
    	exit()

    elif "time" in command:
        say(ctime())


    elif 'what up' in command:
        say('Just doing my thing')
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            say(str(res.json()['joke']))
        else:
            say('oops!I ran out of jokes')

    elif 'weather' in command:
        forecast = forecastio.load_forecast(wapi_key, lat, lng)
        byHour = forecast.hourly()
        say(byHour.summary)

    elif "where is" in command:
        data = re.split('\\bis \\b',command)[-1]
        l2=data
        location = data.replace(' ','+')
        mixer.music.load('blank.mp3')
        say("Hold on, I will show you where   " + l2 + " is.")
        webbrowser.open('https://www.google.nl/maps/place/' + location + '/&amp;')
        time.sleep(4)
       
    else:
        response = chatbot.get_response(command)
        answer=str(response)
        say(answer)
        



say('Hello, How may I help You?')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())

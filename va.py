'''
Building our Virtual Assistant to perform general tasks
1)Making a Conservation,2)Telling time3)Opening browser/webpages
4)Locating maps5)Sending email and so on...
'''
from gtts import gTTS #pip install gtts
import playsound #pip install playsound==1.2.2
#we will use speechrecognition module
import speech_recognition as sr #pip install SpeechRecognition pip install pyaudio
from time import ctime
import os
import uuid
import smtplib

import webbrowser #to open any websites
import re #regular expressions  -->to find/search patterns in a string

#Create a function to make it listens

def listen():
    """Listening function to respond what we speak"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Start talking now...") #own statement
        audio = r.listen(source,phrase_time_limit=5) #time limit is user interest
    data=""
    #Exception Handling
    try:
        data = r.recognize_google(audio,language='en-US')
        print("You said:"+data)
    except sr.UnknownValueError:
        print("I cannot hear you speak louder")
    except sr.RequestError as e:
        print("Request Failed")
    #tts = gTTS(text = data,lang='en')
    #tts.save("speech.mp3")
    #playsound.playsound('speech.mp3')
    return data

#We will define a function to respond back
def respond(String):
    """Function to respond back"""
    tts = gTTS(text = String,lang='en')
    tts.save("speech.mp3")
    filename = "Speech%s.mp3"%str(uuid.uuid4())
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

#Virtual Assistant actions
def virtual_assistant(data):
    """give your actions"""
    if "how are you" in data:
        listening = True
        respond("Good and doing well")

    elif "are you hungry" in data:
        listening = True
        respond("Yes but i can wait...")

    elif "time" in data:
        listening = True
        respond(ctime())
        
    elif "open google"in data.lower():
        listening = True
        url = "https://www.google.com/"
        webbrowser.open(url)
        respond("Success")

    elif "locate" in data:
        listening = True
        webbrowser.open('https://www.google.com/maps/search/'+
                        data.replace("locate",""))
        result = "Located"
        respond("Located {}".format(data.replace("locate","")))

    elif "search google" in data.casefold():
        listening = True
        reg_ex = re.search('search google(.*)',data.casefold())
        print(data)
        url = "https://www.google.com/search?q="
        if reg_ex:
            sub = reg_ex.group(1)
            print(sub,type(sub))
        webbrowser.open(url + sub)
        result = "Success"
        respond("Search for {} complete".format(sub))

    #email -->you need to frst create gmail app passcode

    elif "email" in data:
        listening = True
        respond("Whom should i send email to?")
        to = listen()
        edict = {'hello':'saketh@codegnan.com','new':''} #give mail ids
        toaddr = edict[to]
        respond("What is the Subject?")
        subject = listen()
        respond("What should i tell that person?")
        message = listen()
        content = 'Subject :{}\n\n{}'.format(subject,message)

        #init gmail SMTP
        mail = smtplib.SMTP('smtp.gmail.com',587)
        #identify the server
        mail.ehlo()
        mail.starttls()
        #login
        mail.login('','') #enter mailid and app password make sure you enable less secure app access
        mail.sendmail('',toaddr,content) #enter your gmail username
        mail.close()
        respond('Email Sent')

    elif "stop talking" in data:
        listening =False
        respond("Okay signing off for today take care")
    
        
    try:
        return listening
    except UnboundLocalError:
        print("Timedout")
respond("Hey Codegnan how are you?") #frst greeting

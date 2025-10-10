import datetime
from gtts import gTTS
import pygame
import os
import speech_recognition as sr

from g7 import model1                                           # This is Model to generate Output...            

recog = sr.Recognizer()              
mic = sr.Microphone()                
pygame.mixer.init()

sunn = True
language = 'en'  # use 'hi' for Hindi
def greet2():
        hour = datetime.datetime.now().hour
        if hour < 12:
            return "Good Morning"
        elif hour < 18:
            return "Good Afternoon"
        else:
            return "Good Evening"

def speak(text):
            try:
                tts = gTTS(text=text, lang=language) #             use 'hi' for Hindi
                tts.save("response.mp3")
                pygame.mixer.music.load("response.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pass
                os.remove("response.mp3")
            except Exception as e:
                error = f"Speech synthesis error: {str(e)}"
                print(f"Error: {error}")
                speak("Sorry Error4")

def get_input():
        with mic as source:
            recog.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recog.listen(source, timeout=3, phrase_time_limit=5)
                text = recog.recognize_google(audio)
                if text.strip():
                    print(text)
                    return text

            except sr.WaitTimeoutError:
                print("~",end="")
            except sr.UnknownValueError:
                print("~",end="")
            except sr.RequestError:
                print("~",end="")

        typed = input()
        return typed if typed.strip() else None

def get_input2():
        typed = input()
        return typed if typed.strip() else None
    

if __name__ == "__main__":
    for i in range(25):
        if i == 18:
            print('This is Developed by Abhay Pratap Singh'.center(150))
        print()
        
    f = open("chat.txt",'r+')
    f.seek(0)
    chats = f.read()
    now = datetime.datetime.now()
    today = datetime.date.today()
    f.write(f'\n----------------------------------------------------   {today.strftime('%B %d, %Y'), now.strftime('%H:%M:%S')}   ---------------------------------- LISA 1.4')
    
    
    print("LISA Started. Type 'exit' to quit.".center(150))

    g2 = greet2()
    
    print(f"LISA: {g2}")
    speak(f"{g2} Sir")
    
    while True:
        print("You : ", end="")
        if sunn:
            user_input = get_input().lower()    # For Voice Input
        else:
            user_input = get_input2().lower()   # For Text Input
        
        if user_input is None:
            continue
        elif user_input == "english":
            language = 'en'
            speak("Language changed to English")
            continue
        elif user_input == "hindi":
            language = 'hi'
            speak("Language changed to Hindi")
            continue
        elif user_input == "text mode":
            sunn = False
            speak("Text mode activated")
            continue
        elif user_input == "voice mode":
            sunn = True
            speak("Voice mode activated")
            continue
        else:
        
            ans = model1(user_input)   # This is Model to generate Output...
            
            print("LISA:",ans)
            speak(ans)
            f.write("\nYou  : "+user_input)
            f.write("\nLISA : "+ans)

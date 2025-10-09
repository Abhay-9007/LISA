# It is complete if i only integrate speaking and implement proper backend in it                                8th Augut 2025
import webbrowser
import datetime
import random
import sys
import speech_recognition as sr      # for listening
from gtts import gTTS                # for speaking 
import pygame                        # for speaking {helps}
import os                            # for deleting files
from datetime import date

recog = sr.Recognizer()              # for listening audio
mic = sr.Microphone()                # for using microphone
pygame.mixer.init()

lf = ["remind.txt"]
wanted = ['to','remind','me','reminder','kill','try','about','solve','solving','calculate','calculation','open','insta','instagram','yt','youtube','google','chatgtp','gtp','chat','search','browse','give','display','print','show','say','speek','task','tasks','note','notes','add', 'date', 'time', 'i love you', 'addn', 'addt', 'count', 'search', 'open', 'browse', 'play', 'solve', '', 'updates', 'hi', 'hello', 'hey', 'wassup', 'mf', 'fuck', 'nigga', 'hoe', 'bitch', 'dog', 'shit', 'fuck you', 'randi', 'motherfucker', 'bye', 'goodbye', 'see you later', 'see you', 'see you around', 'quit', 'exit', 'q', 'search', 'browse', 'google', 'delete', 'remove', 'pop', 'clear', 'wipe', 'delete all', 'remove all', 'clear all', 'wipe it']
bad_word = ["mf","fuck","nigga","hoe","bitch","dog","shit","fuck you","randi","motherfucker"]

def greet():
    
    greetings = [
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?",
        "Hey! What's on your mind?"
    ]
    return random.choice(greetings)

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%H:%M:%S')}"

def get_date():
    today = datetime.date.today()
    return f"Today's date is {today.strftime('%B %d, %Y')}"

def exit_assistant():
    print("Goodbye! Have a great day. 👋")
    speak("Goodbye! Have a great day.")
    sys.exit()
    
def speak(text):
        #print(f"AI: {text}")
        try:
            tts = gTTS(text=text, lang='en') #             use 'hi' for Hindi
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

    # If no voice → fallback to text
    typed = input()
    return typed if typed.strip() else None
def listen1():                                         #das ist für hürren...
    with sr.Microphone() as source:
        recog.adjust_for_ambient_noise(source)
        audio = recog.listen(source)
        
        try:
            text = recog.recognize_google(audio)
            if not text:
                return None
            print(text)
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            #return listen()
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None

def listen2():
    speak("Listening...")
    with mic as source:
        #recog.adjust_for_ambient_noise(source)
        audio = recog.listen(source)
        #print(audio)
        try:
            text = recog.recognize_google(audio)
            if not text:
                return None
            print("text = none :" + text)
            return text
        except:  # noqa: E722
            speak("Sorry i can't hear that.")
            return None

def greet2():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"
def swears():
    toSay= ["Nigga, Don't play with me.",
            "That's a mean thing to say.",
            "Wipe your ass out! Motherfucker",
            "You're a piece of shit.",
            "You better Run Motherfucker",
            "I'm Gonna Skin You alive."
    ]
    return random.choice(toSay)

def days_remains():
    today = date.today()
    target = date(2026, 1, 1)
    dl = (target - today).days
    ans = f"You have {dl} days left."
    return ans

def generateCommand(x):
    command = []
    con = ''
    if "'" in x:
        con = x.split("'")[1]
    elif '"' in x:
        con = x.split('"')[1]
    if con == '':
        con = input('    What: ')
    #print(con)         
    x = x.lower().strip()    
    x = x.split(" ")
    #print(x)
    num = -1
    for i in x:
        try:
            num = int(i)
        except: # noqa: E722
            pass
        if i in wanted and i != "":
            command.append(i) 
    command = " ".join(command)
    #print("this is the number :", num)
    return process_command(command, con, num)

def process_command(command, con, num):
    if 'clear' in command or "erase" in command:
        if 'notes' in command:
            f = open("notes.txt", "w")
            lf[0] = "notes.txt"
            f.seek(0)
            f.write("")
            f.close()
            return "Notes Cleared"
        elif 'tasks' in command or 'task' in command:
            f = open("task.txt", "w")
            lf[0] = "task.txt"
            f.seek(0)
            f.write("")
            f.close()
            return "Tasks Cleared"
        elif 'remind' in command or 'reminder' in command:
            f = open("remind.txt", "w")
            lf[0] = "remind.txt"
            f.seek(0)
            f.write("")
            f.close()
            return "Reminders Cleared"
        else:
            return "No Specific File Mentioned to Clear"
    elif 'pop' in command or 'delete' in command or 'del' in command:
        lf[0] = "remind.txt"
        f = open(lf[0], "r")
        f.seek(0)
        data = f.readlines()
        if num == -1:
            num = len(data)-1
        deleted = data.pop(num)
        data = "".join(data)
        f.close()
        f = open(lf[0], "w")
        f.seek(0)
        f.write(data)
        f.close()
        if deleted:
            return deleted + " : Deleted..." 
        return "Nothing to delete"
    
    elif 'remind' in command and 'me' in command and 'to' in command:
        f = open("remind.txt", "a+")
        lf[0] = "remind.txt"
        f.write(con + "\n")
        return "Added"
    
    elif 'remind' in command and 'me' in command:
        f = open("remind.txt", "r+")
        lf[0] = "remind.txt"
        f.seek(0)
        return f.read()
    
    elif 'add' in command:
        if 'reminder' in command or 'remind' in command:
            f = open("remind.txt", "a+")
            lf[0] = "remind.txt"
            f.write(con + "\n")
            return "Done" 
    
        elif "tasks" in command or 'task' in command:
            f = open("task.txt", "a+")
            lf[0] = "task.txt"
            f.write(con + "\n")
            return "Done"
        elif 'notes' in command or 'note' in command:
            f = open("notes.txt", "a+")
            lf[0] = "notes.txt"
            f.write(con + "\n")
            return "Done"
        else:
            
            f = open(lf[0], "a+")
            f.write(con + "\n")
            lf[0] = "notes.txt"
            return "Done"
        
    elif 'print' in command or 'show' in command or 'display' in command or 'give' in command:
        if 'reminder' in command or 'remind' in command:
            f = open("remind.txt", "a+")
            lf[0] = "remind.txt"
            f.seek(0)
            return f.read() 
        
        elif "tasks" in command or 'task' in command:
            f = open("task.txt", "r+")
            lf[0] = "task.txt"
            f.seek(0)
            return f.read()
        elif 'notes' in command or 'note' in command:
            f = open("notes.txt", "r+")
            lf[0] = "notes.txt"
            f.seek(0)
            return f.read()
        
        else:
            f = open(lf[0], "r+")
            lf[0] = "notes.txt"
            f.seek(0)
            return f.read()
        
    elif 'say' in command or 'speak' in command:
        return con

    elif 'about' in command:
        f = open("about.txt", "r")
        f.seek(0)
        return f.read()
        
    elif 'date' in command:
        return get_date()
    
    elif 'time' in command:
        return get_time()
    
    elif 'search' in command or 'browse' in command or 'google' in command:
        query = con.replace("search", "").replace("google", "").replace("browse", "").strip()
        webbrowser.open(f"https://google.com/search?q={query}")
        return f"Searching for {query}"
    
    elif 'play' in command:
        query = con.replace("play", "").strip()
        webbrowser.get("open -a 'Brave Browser' %s").open(f"https://www.youtube.com/results?search_query={query}")
        return f"Playing {query} on YouTube"
    
    elif "count" in command:
        return days_remains()
    
    elif command in bad_word:
        return swears()
    
    elif 'solve' in command or 'calculate' in command or 'calculation' in command or 'solving' in command:
        t = con.replace('solve', '').replace('calculate', '').replace('calculation', '').replace('solving', '').strip()
        ans = str(eval(t))
        return ans
    
    elif "kill" in command or "bye" in command or "goodbye" in command or "see you later" in command or "see you" in command or "see you around" in command or "quit" in command or "exit" in command or "q" in command:
        exit_assistant()
    elif "open" in command:
        if "youtube" in command or "yt" in command:
            webbrowser.get("open -a 'Brave Browser' %s").open("https://www.youtube.com")
            #webbrowser.open("https://youtube.com")
            return "Opening YouTube"
        elif "instagram" in command or "insta" in command:
            webbrowser.get("open -a 'Brave Browser' %s").open("https://instagram.com")
            return "Opening Instagram but Do not waste your time there."
        elif "chatgtp" in command or "gtp" in command or "chat" in command:
            webbrowser.open("https://www.chatgpt.com")
            return "Opening ChatGPT"
        else:
            webbrowser.open("https://google.com")
            return "Opening Google"
    
    elif "hi" in command or "hello" in command or "hey" in command or "wassup" in command:
        return greet()
    elif command == " ":
        pass 
    else:
        return "Oops"
# MAIN LOOP
if __name__ == "__main__":
    for i in range(9):
        print()
        
    f = open("chat.txt",'r+')
    f.seek(0)
    chats = f.read()
    now = datetime.datetime.now()
    today = datetime.date.today()
    f.write(f'\n-------------------   {today.strftime('%B %d, %Y'), now.strftime('%H:%M:%S')}   --------------- LISA 1.30')
    
    
    print("LISA Started. Type 'exit' to quit.".center(150))
    g1 = greet()
    g2 = greet2()
    print(f"LISA: {g2}")

    #print(f"LISA: {g1}")
    speak(f"{g2} Sir")
    #speak(f"{g1}")
    while True:
        print("You : ", end="")
        #comm1 = listen1()                          # For voice input
        #comm2 = input()                            # For text input
        user_input = get_input() #listen1() if listen1() is not None else input()
        if user_input is None:
            #speak("Sorry, I didn't catch that.")
            continue
        ans = generateCommand(user_input)   #process_command(user_input) i commented it
        if ans is None:
            speak("Empty command.")
        print("LISA:",ans)
        speak(ans)
        f.write("\nYou  : "+user_input)
        f.write("\nLISA : "+ans)


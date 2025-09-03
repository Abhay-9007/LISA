

import webbrowser
import datetime
import random
import sys
import speech_recognition as sr
from gtts import gTTS
import os

# Only load pygame locally, not on Railway
if not os.environ.get("RAILWAY_ENVIRONMENT"):
    try:
        import pygame
        pygame.init()
        pygame.mixer.init()
    except ImportError:
        pass
        
import os
from datetime import date
import sqlite3

# 🎤 Setup
recog = sr.Recognizer()
mic = sr.Microphone()

# 📂 Database Setup
conn = sqlite3.connect("assistant.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
conn.commit()

# 🔑 Keywords
wanted = ['solve','solving','calculate','calculation','open','insta','instagram','yt','youtube','google','chatgtp','gtp','chat','search','browse','give','display','print','show','say','speek','task','tasks','note','notes','add','date','time','i love you','addn','addt','count','play','updates','hi','hello','hey','wassup','mf','fuck','nigga','hoe','bitch','dog','shit','fuck you','randi','motherfucker','bye','goodbye','see you later','see you','see you around','quit','exit','q','delete','remove','pop','clear','wipe','delete all','remove all','clear all','wipe it']
bad_word = ["mf","fuck","nigga","hoe","bitch","dog","shit","fuck you","randi","motherfucker"]


def model(text):
    # 📢 Speak
     def speak(text):
         pass
    #     try:
    #         tts = gTTS(text=text, lang='en')
    #         tts.save("response.mp3")
    #         #pygame.mixer.music.load("response.mp3")
    #         #pygame.mixer.music.play()
    #         while pygame.mixer.music.get_busy():
    #             pass
    #         os.remove("response.mp3")
    #     except Exception as e:
    #         print(f"Error: {e}")

    # 👋 Greet
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

    def swears():
        toSay= [
            "Nigga, Don't play with me.",
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
        return f"You have {dl} days left."

    # 🔄 Command Processor
    def generateCommand(x):
        command = []
        con = x
        if "'" in x:
            con = x.split("'")[1]
        elif '"' in x:
            con = x.split('"')[1]
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
        # 🗑 Clear
        if 'clear' in command or "erase" in command:
            if 'notes' in command:
                cursor.execute("DELETE FROM notes")
                conn.commit()
                return "Notes Cleared"
            elif 'tasks' in command or 'task' in command:
                cursor.execute("DELETE FROM tasks")
                conn.commit()
                return "Tasks Cleared"
            elif 'remind' in command or 'reminder' in command:
                cursor.execute("DELETE FROM reminders")
                conn.commit()
                return "Reminders Cleared"
            else:
                return "No Specific Section Mentioned to Clear"

        # ❌ Delete
        elif 'pop' in command or 'delete' in command or 'del' in command:
            cursor.execute("SELECT id, text FROM reminders")
            rows = cursor.fetchall()
            if not rows:
                return "Nothing to delete"
            if num == -1:
                num = rows[-1][0]  # delete last
            cursor.execute("DELETE FROM reminders WHERE id=?", (num,))
            conn.commit()
            return f"Deleted reminder {num}"

        # ➕ Add reminder
        elif 'remind' in command and 'me' in command and 'to' in command:
            cursor.execute("INSERT INTO reminders (text) VALUES (?)", (con,))
            conn.commit()
            return "Reminder Added"

        elif 'remind' in command and 'me' in command:
            cursor.execute("SELECT text FROM reminders")
            rows = cursor.fetchall()
            return "\n".join([r[0] for r in rows]) if rows else "No reminders"

        elif 'add' in command:
            if 'reminder' in command or 'remind' in command:
                cursor.execute("INSERT INTO reminders (text) VALUES (?)", (con,))
                conn.commit()
                return "Reminder Added"
            elif "tasks" in command or 'task' in command:
                cursor.execute("INSERT INTO tasks (text) VALUES (?)", (con,))
                conn.commit()
                return "Task Added"
            elif 'notes' in command or 'note' in command:
                cursor.execute("INSERT INTO notes (text) VALUES (?)", (con,))
                conn.commit()
                return "Note Added"
            else:
                cursor.execute("INSERT INTO notes (text) VALUES (?)", (con,))
                conn.commit()
                return "Note Added"

        # 📖 Show data
        elif 'print' in command or 'show' in command or 'display' in command or 'give' in command:
            if 'reminder' in command or 'remind' in command:
                cursor.execute("SELECT text FROM reminders")
                rows = cursor.fetchall()
                return "\n".join([r[0] for r in rows]) if rows else "No reminders"
            elif "tasks" in command or 'task' in command:
                cursor.execute("SELECT text FROM tasks")
                rows = cursor.fetchall()
                return "\n".join([r[0] for r in rows]) if rows else "No tasks"
            elif 'notes' in command or 'note' in command:
                cursor.execute("SELECT text FROM notes")
                rows = cursor.fetchall()
                return "\n".join([r[0] for r in rows]) if rows else "No notes"
            else:
                return "No data found"

        # 🔊 Say
        elif 'say' in command or 'speak' in command:
            return con

        elif 'date' in command:
            return get_date()

        elif 'time' in command:
            return get_time()

        elif 'search' in command or 'browse' in command or 'google' in command:
            query = con.strip()
            webbrowser.open(f"https://google.com/search?q={query}")
            return f"Searching for {query}"

        elif 'play' in command:
            query = con.strip()
            webbrowser.get("open -a 'Brave Browser' %s").open(f"https://www.youtube.com/results?search_query={query}")
            return f"Playing {query} on YouTube"

        elif "count" in command:
            return days_remains()

        elif command in bad_word:
            return swears()

        elif 'solve' in command or 'calculate' in command or 'calculation' in command or 'solving' in command:
            t = con.strip().replace('solve','').replace('calculate','').replace('calculation','').replace('solving','')
            if con == '':
                return "No calculation provided"
            try:
                ans = str(eval(t))
                return ans
            except:  # noqa: E722
                return "Error in calculation"

        elif "kill" in command or "bye" in command or "goodbye" in command or "see you later" in command or "quit" in command or "exit" in command or "q" in command:
            exit_assistant()

        elif "open" in command:
            if "youtube" in command or "yt" in command:
                webbrowser.get("open -a 'Brave Browser' %s").open("https://www.youtube.com")
                return "Opening YouTube"
            elif "instagram" in command or "insta" in command:
                webbrowser.get("open -a 'Brave Browser' %s").open("https://instagram.com")
                return "Opening Instagram"
            elif "chatgtp" in command or "gtp" in command or "chat" in command:
                webbrowser.open("https://chat.openai.com")
                return "Opening ChatGPT"
            else:
                webbrowser.open("https://google.com")
                return "Opening Google"

        elif "hi" in command or "hello" in command or "hey" in command or "wassup" in command:
            return greet()

        else:
            return "Oops, I don't understand."

    # ----------------- MAIN LOOP -------------------
    now = datetime.datetime.now()
    today = datetime.date.today()
    cursor.execute("INSERT INTO chat (role, message) VALUES (?, ?)", ("System", f"--- {today}, {now} --- LISA 2.0 ---"))
    conn.commit()

    # User input → process
    user_input = text
    ans = generateCommand(user_input)

    # Save chat
    cursor.execute("INSERT INTO chat (role, message) VALUES (?, ?)", ("You", user_input))
    cursor.execute("INSERT INTO chat (role, message) VALUES (?, ?)", ("LISA", ans))
    conn.commit()

    # Speak
    #speak(ans)
    return ans


#print(model('give me task') ) # Test run

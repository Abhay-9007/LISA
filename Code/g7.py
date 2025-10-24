# Have to integrate Backend for this                                                            8th Augut 2025
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

lf = ["remind.txt"]                  # this is last file opened...
wanted = ['gate.env','daily.env','mid.env','file','day','weekly','monthly','normal','daily', 'week', 'month', 'other', 'general','to','remind','me','reminder','kill','try','about','solve','solving','calculate','calculation','open','insta','instagram','yt','youtube','google','chatgtp','gtp','chat','search','browse','give','display','print','show','say','speek','task','tasks','note','notes','add', 'date', 'time', 'i love you', 'addn', 'addt', 'count', 'search', 'open', 'browse', 'play', 'solve', '', 'updates', 'hi', 'hello', 'hey', 'wassup', 'mf', 'fuck', 'nigga', 'hoe', 'bitch', 'dog', 'shit', 'fuck you', 'randi', 'motherfucker', 'bye', 'goodbye', 'see you later', 'see you', 'see you around', 'quit', 'exit', 'q', 'search', 'browse', 'google', 'delete', 'remove', 'pop', 'clear', 'wipe', 'delete all', 'remove all', 'clear all', 'wipe it']
bad_word = ['''All the Bad words must be hare''']

def model1(user_input):

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
    
    def encryption(inp, val=1):
        if not inp:
            return ""
        out = ""
        for i in inp:
            if i in ('"', "'"):
                out += i  
            else:
                out += chr(ord(i) + val)
            val += 1
        return out

    def decryption(inp, val=1):
        if not inp:
            return ""
        out = ""
        for i in inp:
            if i in ('"', "'"):
                out += i  
            else:
                try:
                    out += chr(ord(i) - val)
                except ValueError:
                    out += "?"  
            val += 1
        return out
    
    def open_video(url):
        webbrowser.get("open -a 'Brave Browser' %s").open(url) 
        
    def print_data(l1):
        for i in l1:
            print(i)
            
    def xxx(input='general'):
        options = ['daily', 'week', 'month', 'other', 'general',]
        if input not in options:
            return "Invalid option. Choose from: " + ", ".join(options)
        else:
            nig = "["+input+"]"
            
        f = open("remind.txt", "r+")
        f.seek(0)
        textd = f.readlines()
        
        if not textd:
            return "Empty"
        ans_ = []
        for i in textd:
            temp = i.split(':')
            if temp[0] == nig:
                ans_ = temp[1:]
                break
        f_ans = ""
        count = 0
        for i in ans_:
            f_ans += f"{count}. {i.strip()}\n"
            count+=1
        return "\n"+f_ans.strip()
    
    def aaa(x,y):
        if x not in ['daily', 'week', 'month', 'other', 'general']:
            return "Invalid Option."
        if not y:
            return "done"
        
        f = open("remind.txt", "a+")
        f.seek(0)
        remind_data = f.readlines()
        f.close()
        f = open("remind.txt", "w")
        
        if not remind_data:
            return "Empty"
        
        for i in range(len(remind_data)):
            if remind_data[i].startswith("["+x+"]"):
                remind_data[i] = remind_data[i].strip() + ':'+y + "\n"
                f.seek(0)
                f.writelines(remind_data)
                return y + " Added in "+ x + " Section."
        
        return remind_data
    
    def open_file(file_name):
        try:
            f = open(file_name, 'r')
            content = f.read()
            f.close()
        except: # noqa: E722
            return "File not found."
        return content
    
    def generateCommand(x,con):
        if x is None:
            return "Nigga, what the fuck you want me to do?"
        
        command = []
        if con is None:
            con = x
            if "'" in x:
                con = x.split("'")[1]
            elif '"' in x:
                con = x.split('"')[1] 
        x = x.lower().strip()    
        x = x.split(" ")
        num = -1
        for i in x:
            try:
                num = int(i)
            except: # noqa: E722
                pass
            if i in wanted and i != "":
                command.append(i) 
        command = " ".join(command)
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
                f.write("\n[daily]:\n[week]:\n[month]:\n[other]:\n[general]:\n")
                f.close()
                return "Reminders Cleared"
            else:
                return "No Specific File Mentioned to Clear"
            
        elif 'open' in command and 'file' in command:
            return open_file(con)
        
        elif 'pop' in command or 'delete' in command or 'del' in command:
            if lf[0] == "remind.txt":
                return "Don't touch the Shit you can't Handle..."
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
                return deleted + "    : is Deleted..." 
            return "Nothing to delete"
        
        elif 'remind' in command and 'me' in command and 'to' in command:
            lf[0] = "remind.txt"
            aaa("other",con)
            return "Added..."
        
        elif 'add' in command:
            if 'reminder' in command or 'remind' in command:
                lf[0] = "remind.txt"
                if 'week' in command or 'weekly' in command:
                    aaa("week",con)
                elif 'month' in command or 'monthly' in command:
                    aaa("month",con)
                elif 'daily' in command or 'day' in command:
                    aaa("daily",con)
                elif 'general' in command or 'normal' in command:
                    aaa("general",con)
                else:
                    aaa("other",con)
                return "Added..."
        
            elif "tasks" in command or 'task' in command:
                f = open("task.txt", "a+")
                lf[0] = "task.txt"
                f.write(con + "\n")
                return "Done"
            
            elif 'notes' in command or 'note' in command:
                f = open("notes.txt", "a+")
                lf[0] = "notes.txt"
                f.write(encryption(con) + "\n")
                return "Done"
                
            else:
                f = open(lf[0], "a+")
                f.write(con + "\n")
                return "Done"
            
        elif 'print' in command or 'show' in command or 'display' in command or 'give' in command:
            if 'remind' in command or 'reminder' in command or 'reminders' in command and 'me' in command:
                lf[0] = "remind.txt"
                if 'week' in command or 'weekly' in command:
                    return xxx("week")
                elif 'month' in command or 'monthly' in command:
                    return xxx("month")
                elif 'daily' in command or 'day' in command:
                    return xxx("daily")
                elif 'general' in command or 'normal' in command:
                    return xxx("general")
                else:
                    return xxx("other")
                
            
            elif "tasks" in command or 'task' in command:
                f = open("task.txt", "r+")
                lf[0] = "task.txt"
                f.seek(0)
                return f.read()
            
            elif 'notes' in command or 'note' in command:
                f = open("notes.txt", "r+")
                lf[0] = "notes.txt"
                f.seek(0)
                return f.read() # decription(f.read())
            
            else:
                return 'Sorry'
            
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
            open_video(f"https://www.youtube.com/results?search_query={query}")
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
            put_file(last_intr)
            exit_assistant()
            
        elif "open" in command:
            # print(command)
            # print(con)
            # print(num)
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
            
            elif "mid.env" in command:
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")  
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")  
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")  
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")   
                return "Opening the Mid-Term Environment."
            
            elif "daily.env" in command:
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")  
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")  
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")  
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")   
                return "Opening the Daily Environment."
            
            elif "gate.env" in command:
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")  
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")  
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")  
                open_video("https://www.youtube.com/watch?v=npnAlIbyknI")   
                return "Opening the GATE Environment."
            
            else:
                webbrowser.open("https://google.com")
                return "Opening Google"
        
        elif "hi" in command or "hello" in command or "hey" in command or "wassup" in command:
            return greet()
        
        elif command == " ":
            pass
        else:
            return random.choice(["Hell No", "Sorry", "Oops"])
    
    # This is File handling part of instractions Stack
    def put_file(data):  # save instructions
        with open("itr.txt", 'w') as f:  # 'w' clears file automatically
            for item in data:
                enc = encryption(item)
                #print("---", enc)
                f.write(enc + '\n')
        return None

    def get_file():  # load instructions
        data2 = []
        with open("itr.txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                dec = decryption(line.strip())  
                data2.append(dec)
        return data2

    last_intr = get_file() 

    def inst_manager(input):
        if input not in last_intr and input not in ['0','1','2']:
            last_intr.append(input)
            if len(last_intr) > 3:
                last_intr.pop(0)
            put_file(last_intr)
        return None

    def get_inst(input):
        if input == '0':
            return last_intr[-1]
        elif input == '1':
            return last_intr[1]
        elif input == '2':
            return last_intr[0]
        else:
            return None
        
    if user_input[0] in ['0','1','2'] and len(user_input.strip()) != 1:
        ans = generateCommand(get_inst(user_input[0]),user_input[2:])
    elif user_input[0] in ['0','1','2']:
        ans = generateCommand(get_inst(user_input[0]),None)
    else:
        ans = generateCommand(user_input,None)
    
    print("Last Instructions :",last_intr)
    
    if ans not in ["Oops", "Sorry", "Hell No"] and user_input[0] not in ['0','1','2']:
        inst_manager(user_input)

    return ans


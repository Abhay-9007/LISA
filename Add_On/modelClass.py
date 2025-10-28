class ModelResponse():
    def __init__(self, userInput: str):
        self.userinput = userInput
        self.output = self.generateOutput(userInput)
        self.lastFile = "remind.txt"
        self.lastInstruction = self.getFile()
        
    def greet() -> str:
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! What's on your mind?"
        ]
        return random.choice(greetings)
    
    def getTime(self) -> str:
        now = datetime.datetime.now()
        return f"the Current time is now {now.strtime('%H:%M:%S')}"
    
    def getDate(self) -> str:
        today = date.today()
        return f"Today's date is {today.strftime('%B %d, %Y')}"
    
    def exitAssistant(self) -> None:
        print("LISA: Goodbye! Have a great day ahead.")
        self.speak("Goodbye! Have a great day ahead.")
        sys.exit()
    
    def speak(self, text: str) -> None:
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
            self.speak("Sorry Error4")
    
    def swars(self) -> str:
        swears = [
            "That's not very nice.",
            "Please watch your language.",
            "Let's keep the conversation respectful.",
            "I'm here to help, not to be insulted.",
            "Let's focus on something positive.",
            "Nigga, Don't play with me.",
            "That's a mean thing to say.",
            "Wipe your ass out! Motherfucker",
            "You're a piece of shit.",
            "You better Run Motherfucker",
            "I'm Gonna Skin You alive."
        ]
        return random.choice(swears)
    
    def dayRemains(self) -> str:
        today = date.today()
        target = date(2026, 1, 1)
        dl = (target - today).days
        ans = f"You have {dl} days left."
        return ans
    
    def encryption(self,input: str, val=1) -> str:
        if not input:
            return ""
        output = ""
        for i in input:
            if i in ('"', "'"):
                output += i  # keep quotes
            else:
                output += chr(ord(i) + val)
            val += 1
        return output
    
    def decryption(self,input: str, val=1) -> str:
        if not input:
            return ""
        output = ""
        for i in input:
            if i in ('"', "'"):
                output += i  # keep quotes
            else:
                output += chr(ord(i) - val)
            val += 1
        return output
    def openVideo(self, url: str) -> None:
        webbrowser.get("open -a 'Brave Browser' %s").open(url)
        return None
    
    def addReminder(self, input='general') -> str:
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
    
    def getReminder(self, catagory='general', input='general') -> str:
        if catagory not in ['daily', 'week', 'month', 'other', 'general']:
            return "Invalid Option."
        if not input:
            return "done"
        
        f = open("remind.txt", "a+")
        f.seek(0)
        remind_data = f.readlines()
        f.close()
        f = open("remind.txt", "w")
        
        if not remind_data:
            return "Empty"
        
        for i in range(len(remind_data)):
            if remind_data[i].startswith("["+catagory+"]"):
                remind_data[i] = remind_data[i].strip() + ':'+ input + "\n"
                f.seek(0)
                f.writelines(remind_data)
                return input + " Added in "+ catagory + " Section."
        
        return remind_data
    
    def openFile(self, filename: str) -> str:
        try:
            f = open(filename, 'r')
            content = f.read()
            f.close()
        except: # noqa: E722
            return "File not found."
        return content
    
    def generateResponse(self) -> str:
        return self.output

    def getFile(self) -> str:
        data2 = []
        with open("itr.txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                dec = self.decryption(line.strip())  
                data2.append(dec)
                
        return data2
    
    def putFile(self, input: list) -> None:
        with open("itr.txt", 'w') as f:
            for i in input:
                enc = self.encryption(i)
                f.write(enc + "\n")
        return None
    
    def instructionManager(self, input: str) -> str | None:
        if input not in self.lastInstruction and input not in ['0','1','2']:
            self.lastInstruction.append(input)
            if len(self.lastInstruction) > 3:
                self.lastInstruction.pop(0)
            self.putFile(self.lastInstruction)
        return None
    
    def getInstruction(self,input: str) -> None | str:
        if input == '0':
            return self.lastInstruction[-1]
        elif input == '1':
            return self.lastInstruction[1]
        elif input == '2':
            return self.lastInstruction[0]
        else:
            return None
    
    def generateOutput(self, userInput: str) -> str:
        command = UserInput().getCommand(userInput)
        con = UserInput().getIntution(userInput)
        num = UserInput().getNum(userInput)
        
        if 'clear' in command or "erase" in command:
            if 'notes' in command:
                f = open("notes.txt", "w")
                self.lastFile = "notes.txt"
                f.seek(0)
                f.write("")
                f.close()
                return "Notes Cleared"
            elif 'tasks' in command or 'task' in command:
                f = open("task.txt", "w")
                self.lastFile = "task.txt"
                f.seek(0)
                f.write("")
                f.close()
                return "Tasks Cleared"
            elif 'remind' in command or 'reminder' in command:
                f = open("remind.txt", "w")
                self.lastFile = "remind.txt"
                f.seek(0)
                f.write("\n[daily]:\n[week]:\n[month]:\n[other]:\n[general]:\n")
                f.close()
                return "Reminders Cleared"
            else:
                return "No Specific File Mentioned to Clear"
            
        elif 'open' in command and 'file' in command:
            return self.openFile(con)
        
        elif 'pop' in command or 'delete' in command or 'del' in command:
            if self.lastFile == "remind.txt":
                return "Don't touch the Shit you can't Handle..."
            f = open(self.lastFile, "r")
            f.seek(0)
            data = f.readlines()
            if num == -1:
                num = len(data)-1
            deleted = data.pop(num)
            data = "".join(data)
            f.close()
            f = open(self.lastFile, "w")
            f.seek(0)
            f.write(data)
            f.close()
            if deleted:
                return deleted + "    : is Deleted..." 
            return "Nothing to delete"
        
        elif 'remind' in command and 'me' in command and 'to' in command:
            self.lastFile = "remind.txt"
            self.addReminder("other",con)
            return "Added..."
        
        elif 'add' in command:
            if 'reminder' in command or 'remind' in command:
                self.lastFile = "remind.txt"
                if 'week' in command or 'weekly' in command:
                    self.addReminder("week",con)
                elif 'month' in command or 'monthly' in command:
                    self.addReminder("month",con)
                elif 'daily' in command or 'day' in command:
                    self.addReminder("daily",con)
                elif 'general' in command or 'normal' in command:
                    self.addReminder("general",con)
                else:
                    self.addReminder("other",con)
                return "Added..."
        
            elif "tasks" in command or 'task' in command:
                f = open("task.txt", "a+")
                self.lastFile = "task.txt"
                f.write(con + "\n")
                return "Done"
            
            elif 'notes' in command or 'note' in command:
                f = open("notes.txt", "a+")
                self.lastFile = "notes.txt"
                f.write(self.encryption(con) + "\n")
                return "Done"
                
            else:
                f = open(self.lastFile, "a+")
                f.write(con + "\n")
                return "Done"
            
        elif 'print' in command or 'show' in command or 'display' in command or 'give' in command:
            if 'remind' in command or 'reminder' in command or 'reminders' in command and 'me' in command:
                self.lastFile = "remind.txt"
                if 'week' in command or 'weekly' in command:
                    return self.getReminder("week")
                elif 'month' in command or 'monthly' in command:
                    return self.getReminder("month")
                elif 'daily' in command or 'day' in command:
                    return self.getReminder("daily")
                elif 'general' in command or 'normal' in command:
                    return self.getReminder("general")
                else:
                    return self.getReminder("other")
                
            
            elif "tasks" in command or 'task' in command:
                f = open("task.txt", "r+")
                self.lastFile = "task.txt"
                f.seek(0)
                return f.read()
            
            elif 'notes' in command or 'note' in command:
                f = open("notes.txt", "r+")
                self.lastFile = "notes.txt"
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
            return self.getDate()
        
        elif 'time' in command:
            return self.getTime()
        
        elif 'search' in command or 'browse' in command or 'google' in command:
            query = con.replace("search", "").replace("google", "").replace("browse", "").strip()
            webbrowser.open(f"https://google.com/search?q={query}")
            return f"Searching for {query}"
        
        elif 'play' in command:
            query = con.replace("play", "").strip()
            self.openVideo(f"https://www.youtube.com/results?search_query={query}")
            return f"Playing {query} on YouTube"
        
        elif "count" in command:
            return self.dayRemains()
        
        elif command in self.bad_word:
            return self.swars()
        
        elif 'solve' in command or 'calculate' in command or 'calculation' in command or 'solving' in command:
            t = con.replace('solve', '').replace('calculate', '').replace('calculation', '').replace('solving', '').strip()
            ans = str(eval(t))
            return ans
        
        elif "kill" in command or "bye" in command or "goodbye" in command or "see you later" in command or "see you" in command or "see you around" in command or "quit" in command or "exit" in command or "q" in command:
            self.putFile(self.lastInstruction)
            self.exitAssistant()
            
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
            
            elif "mid.env" in command:
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")  
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")  
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")  
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")   
                return "Opening the Mid-Term Environment."
            
            elif "daily.env" in command:
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")  
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")  
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")  
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")   
                return "Opening the Daily Environment."
            
            elif "gate.env" in command:
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")  
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")  
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")  
                self.openVideo("https://www.youtube.com/watch?v=npnAlIbyknI")   
                return "Opening the GATE Environment."
            
            else:
                webbrowser.open("https://google.com")
                return "Opening Google"
        
        elif "hi" in command or "hello" in command or "hey" in command or "wassup" in command:
            return self.greet()
        
        elif command == " ":
            pass
        else:
            return random.choice(["Hell No", "Sorry", "Oops"])

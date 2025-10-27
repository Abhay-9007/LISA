class userInput():
    # "Abhay is a Good Boy" Nigga shut up say this 69 times
    wanted = ['gate.env','daily.env','mid.env','file','day','weekly','monthly','normal','daily', 'week', 'month', 'other', 'general','to','remind','me','reminder','kill','try','about','solve','solving','calculate','calculation','open','insta','instagram','yt','youtube','google','chatgtp','gtp','chat','search','browse','give','display','print','show','say','speek','task','tasks','note','notes','add', 'date', 'time', 'i love you', 'addn', 'addt', 'count', 'search', 'open', 'browse', 'play', 'solve', '', 'updates', 'hi', 'hello', 'hey', 'wassup', 'mf', 'fuck', 'nigga', 'hoe', 'bitch', 'dog', 'shit', 'fuck you', 'randi', 'motherfucker', 'bye', 'goodbye', 'see you later', 'see you', 'see you around', 'quit', 'exit', 'q', 'search', 'browse', 'google', 'delete', 'remove', 'pop', 'clear', 'wipe', 'delete all', 'remove all', 'clear all', 'wipe it']
    greetings = ['hi', 'hello', 'hey', 'wassup']
    farewells = ['bye', 'goodbye', 'see you later', 'see you', 'see you around', 'quit', 'exit', 'q']
    bad_word = ["mf","fuck","nigga","hoe","bitch","dog","shit","fucking","hundin","motherfucker"]
    
    def __init__(self, userText = str(input("Enter your command: "))):
        self.userText = userText
        self.command = self.getCommand(userText)
        self.instution = self.getIntution(userText)
        self.num = self.getNum(userText)
        self.userMood = self.getUserMood(userText)
        
    def colors():
        print("\033[31mRed")
        print("\033[32mGreen")
        print("\033[33mYellow")
        print("\033[34mBlue")
        print("\033[35mPurple")
        print("\033[36mCyan")
        print("\033[37mWhite")
        print("\033[0m")
    
    def printAll(self) -> None: 
        print("\033[32m-------------------------------------------------------------------------------------------",)
        print("User Text      : ", self.userText)
        print("Command        : ", self.command)
        print("Instution      : ", self.instution)
        print("Is Digit       : ", self.num)
        print("User Mood      : ", self.userMood)
        print("-------------------------------------------------------------------------------------------",end="")
        print("\033[0m") #This is to reset the color
        return None
    
    def getCommand(self, userText: str) -> list:
        if userText is None:
            return "Oops"
        
        command = [] 
        userText = userText.lower().strip()    
        userText = userText.split(" ")
        for i in userText:
            if i in self.wanted and i != "":
                command.append(i) 
        command = " ".join(command)
        
        return command
    
    def getNum(self, userText):
        num = -1
        for i in userText:
            try:
                num = int(i)
            except: # noqa: E722
                pass
        return num

    def getIntution(self,userText: str) -> str:
        con = userText
        if "'" in userText:
            con = userText.split("'")[1]
        elif '"' in userText:
            con = userText.split('"')[1]
        
        return con
    
    def getUserMood(self, userText: str) -> str:
        x = userText.lower().strip()
        x = x.split(" ")
        greet = 0
        farewell = 0
        
        for i in x:
            if i in self.bad_word:
                return "angry"
            elif i in self.greetings:
                greet+=1
            elif i in self.farewells:
                farewell+=1
            
        if greet > 0:
            return "happy"
        elif farewell > 0:
            return "sad"
            
        return "neutral"
    
    
    
    
    
ans = userInput().printAll()
print(ans)
#userInput.colors()



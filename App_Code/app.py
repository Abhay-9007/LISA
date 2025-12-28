# Date is 6th Dec 2025, 
# A desprate attempt to run LISA in my phone 24*7...
# Thing I do for LOVE...
# on 19 dec 2025 lisa is reconsidered...
'''
---------------- Things to add in this Code. ---------------
1. WebBrowsing is not working.                -
2. Content selection of limited.
3. Reminders must be added.                   -
4. Monolog is not working.
5. UI must be improved.
6. Language is not as is coded.
7. Make her responsis funny.
8. Update Swear Function.                     -
9. More File added section for partition of new things.         -
10. Use Classes to achive more effictive answer.
11. Notes are not readable {might be encrypted.}                -
12. integrate this code with my new code base.
13. Try to sell if for real money...***
14. Make A file on which ChatGPT has the full access to read a nd write. {For using  versatile functoins.}{And this is soo cool}
15. Make a log reminder file to log a real crazy thing to have.     
16. Money manager.
17. better version of monolog.
-> for improvement there should be a seperate page to manage my money manager and monolog feature.
    as also it will contribute in my other projects in Web D.
'''

'''
----------- NEW THINGS TO TRY --------------
1. Add a stable database.
2. use any type of AI to content selection, command prioritization, flexible Answers {Non robotic}.
3. Add more API's.
4. Use Animations in UI.
'''
# app.py
from flask import Flask, request, render_template, jsonify
import webbrowser
import datetime
import random
import os
from datetime import date

app = Flask(__name__, static_folder="static", template_folder="templates")

# -------------------------
# Utility: safe file ensure
# -------------------------
def ensure_files():
    files_defaults = {
        "remind.txt": "",
        "notes.txt": "",
        "task.txt": "",
        "about.txt": "LISA 1.4 - Web assistant adapted by integration.",
        "itr.txt": ""
    }
    for fname, content in files_defaults.items():
        if not os.path.exists(fname):
            with open(fname, "w", encoding="utf-8") as f:
                f.write(content)

ensure_files()

# =========================
# Adapted model1 (from file 2)
# =========================
wanted = ['monolog','gate.env','daily.env','mid.env','file','day','reminders','to','remind','me','reminder','kill','try','about','solve','solving','calculate','calculation','open','insta','instagram','yt','youtube','google','chatgtp','gtp','chat','search','browse','give','display','print','show','say','speek','task','tasks','note','notes','add', 'date', 'time', 'addn', 'addt', 'count', 'search', 'open', 'browse', 'play', 'solve', 'updates', 'hi', 'hello', 'hey', 'wassup', 'bye', 'goodbye', 'quit', 'exit', 'q', 'search', 'browse', 'google', 'delete', 'remove', 'pop', 'clear', 'wipe']
bad_word = ["mf","fuck","nigga","hoe","bitch","dog","shit","fuckyou","hundin","motherfucker","pussy","asshole"]
listRem = ["dump","personal","todo"]
lastFile = "notes.txt"
# Simple encryption / decryption used by original model
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

# The actual adapted assistant model
def model1(user_input):
    # helper functions (adapted)
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

    def swears():
        toSay= ["Please don't use offensive language.",
                "That's rude. Let's keep it civil.",
                "Chala ja BSDK",
                "Not Funny.",
                "That's rude.",
                "Is that the line where i have to laugh??",
                "Is that how you treat your mother??",
                "This is how molested kids speak.",
                "You better run Mother Fucker.",
                "Nigga please...",
                "That's mean...",
                "You are a piece of shit.",
                "I will Love to skin you alive.",
                "That's not a proper way to speak.",
                "I doubt your Upbringing"]
        return random.choice(toSay)
    
    def open_video(url):
        webbrowser.get("open -a 'Brave Browser' %s").open(url) 
        
    def days_remains():
        today = date.today()
        target = date(2026, 1, 1)
        dl = (target - today).days
        ans = f"You have {dl} days."
        return ans

    # file helpers
    def open_file(file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                global lastFile
                lastFile = file_name
                return f.read()
        except Exception:
            return "File not found."
    def divideRem(name):
        name = name.lower().strip()
        if name in listRem:
            return f"Catagory of {name} already exists."
        else:
            with open("remind.txt","a") as f:
                listRem.append(name)
                f.write(f"[{name}]:\n")
            return f"New catagory of {name} added."

    def addRem(name,content):
        name = name.lower().strip()
        content = content.strip()
        if name not in listRem:
            return f"Catagory of {name} does not exists."
        else:
            with open("remind.txt","r+") as f:
                data = f.readlines()
                f.seek(0)
                newData = []
                for line in data:
                    if line.startswith(f"[{name}]"):
                        line = line.strip() + ':' + content + "\n"
                    newData.append(line)
                f.writelines(newData)
            return f"Added to {name}."
    
    def getRem(name):
        name = name.lower().strip()
        if name not in listRem:
            return f"Catagory of {name} does not exists."
        else:
            with open("remind.txt","r") as f:
                data = f.readlines()
                for line in data:
                    if line.startswith(f"[{name}]"):
                        reminders = line.split(':')[1:]
                        if not reminders or reminders == ['\n']:
                            return "No Reminders Found."
                        ans = []
                        count = 0
                        for i in reminders:
                            ans.append(f"{count}. {i.strip()}")
                            count+=1
                        return "\n".join(ans)


    def allRem():
        with open("remind.txt","r") as f:
            data = f.readlines()
            ans = ""
            for i in data:
                line = i.split(":")
                ans += str(line[0]).replace("[","").replace("]","").strip().capitalize() + " Reminders:\n"
                count = 1
                for rem in line[1:]:
                    if rem == "" or rem.strip() == "":
                        continue
                    ans +=  f"{count} {rem.strip()}" + "\n"
                    count += 1
                ans += "\n"
                

            return ans.strip()

    def removeRem(name, num):
        name = name.lower().strip()
        if name not in listRem:
            return f"Catagory of {name} does not exists."
        else:
            with open("remind.txt","r+") as f:
                data = f.readlines()
                f.seek(0)
                newData = []
                for line in data:
                    if line.startswith(f"[{name}]"):
                        reminders = line.split(':')
                        remList = reminders[1:]
                        if num < 0 or num >= len(remList):
                            return "Invalid reminder number."
                        remList.pop(num)
                        line = reminders[0] + ':' + ':'.join(remList) + "\n"
                    newData.append(line)
                f.writelines(newData)
            return f"Removed reminder {num} from {name}."

    def deleteRem(name):
        name = name.lower().strip()
        if name not in listRem:
            return f"Catagory of {name} does not exists."
        else:
            with open("remind.txt","r+") as f:
                data = f.readlines()
                f.seek(0)
                newData = []
                for line in data:
                    if not line.startswith(f"[{name}]"):
                        newData.append(line)
                f.writelines(newData)
            listRem.remove(name)
            return f"{name} Deleted."

    def emptyRem(name):
        name = name.lower().strip()
        if name not in listRem:
            return f"Catagory of {name} does not exists."
        else:
            with open("remind.txt","r+") as f:
                data = f.readlines()
                f.seek(0)
                newData = []
                for line in data:
                    if line.startswith(f"[{name}]"):
                        line = f"[{name}]:\n"
                    newData.append(line)
                f.writelines(newData)
            return f"Deleted all reminders from {name}."

    def generateCommand(x,con):
        if x is None:
            return "I didn't get that. Can you rephrase?"
        command = []
        if con is None:
            con = x
            if "'" in x:
                con = x.split("'")[1]
            elif '"' in x:
                con = x.split('"')[1]
        for i in con.split():
            if i.lower() in bad_word:
                return swears()
        x_proc = x.lower().strip().split()
        num = -1
        for i in x_proc:
            try:
                num = int(i)
            except Exception:
                pass
            if i in wanted and i != "" or i in listRem:
                command.append(i)
        command = " ".join(command)
        print("----------------------------------------------------------------------------")
        print(f"|   The command is :    {command}\n|   The context is :    {con}\n|   The number  is :    {num}")
        print("----------------------------------------------------------------------------")
        return process_command(command, con, num)

    def process_command(command, con, num):
        global lastFile
        # Clear commands
        if 'clear' in command or "erase" in command:
            if 'notes' in command:
                lastFile = "notes.txt"
                with open("notes.txt","w",encoding='utf-8') as f:
                    f.write("")
                return "Notes cleared."
            elif 'tasks' in command or 'task' in command:
                lastFile = "task.txt"
                with open("task.txt","w",encoding='utf-8') as f:
                    f.write("")
                return "Tasks cleared."
            else:
                return "No specific file mentioned to clear."

        # File open
        elif 'open' in command and 'file' in command:
            lastFile = con.replace("open","").replace("file","").strip()
            return open_file(con)

        elif "reminder" in command or "remind" in command or "reminders" in command:
            lastFile = "remind.txt"
            if "add" in command:
                for i in listRem:
                    if i in command:
                        return addRem(i, con)
                return addRem("dump", con)
            elif "give" in command or "show" in command or "print" in command or "display" in command:
                for i in listRem:
                    if i in command:
                        return getRem(i)
                return allRem()
            elif 'remove' in command or 'delete' in command or 'pop' in command or 'clear' in command or 'erase' in command or 'wipe' in command:
                if 'all' in command:
                    for i in listRem:
                        if i in command:
                            return deleteRem(i)
                    return "Specify which reminders to clear."
                else:
                    for i in listRem:
                        if i in command:
                            if num == -1:
                                return "Specify which reminder number to remove."
                            return removeRem(i, num)
                    return "Specify which reminders to remove from."
            elif "me" in command:
                return allRem()
            elif "me" in command and "to" in command:
                return addRem("dump",con)
            else:
                return "What do you want to do with reminders?"

        # pop/delete
        elif 'pop' in command or 'delete' in command or 'del' in command:
            # basic handling for task/notes
            
            if lastFile is None:
                return "Specify tasks or notes to delete from."
            try:
                with open(lastFile, "r", encoding='utf-8') as f:
                    data = f.readlines()
            except Exception:
                return "File not found."
            
            if num == -1:
                num = len(data)-1
            if 0 <= num < len(data):
                deleted = data.pop(num)
                with open(lastFile, "w", encoding='utf-8') as f:
                    f.writelines(data)
                return f"Deleted: {deleted.strip()}"
            return "Nothing to delete."

        elif 'add' in command:
            if "tasks" in command or 'task' in command:
                lastFile = "task.txt"
                with open("task.txt", "a", encoding='utf-8') as f:
                    f.write(con + "\n")
                return "Task added."
            elif 'notes' in command or 'note' in command:
                lastFile = "notes.txt"
                with open("notes.txt", "a", encoding='utf-8') as f:
                    f.write(encryption(con) + "\n")
                return "Note saved."
            else:
                with open("task.txt", "a", encoding='utf-8') as f:
                    f.write(con + "\n")
                return "Added."

        elif 'print' in command or 'show' in command or 'display' in command or 'give' in command:
            if "tasks" in command or 'task' in command:
                lastFile = "task.txt"
                return open_file("task.txt")
            elif 'notes' in command or 'note' in command:
                lastFile = "notes.txt"
                return open_file("notes.txt")
            else:
                return 'Nothing specific found to display.'

        elif 'say' in command or 'speak' in command:
            return con

        elif 'about' in command:
            return open_file("about.txt")

        elif 'date' in command:
            return get_date()

        elif 'time' in command:
            return get_time()

        elif 'search' in command or 'browse' in command or 'google' in command:
            query = con.replace("search", "").replace("google", "").replace("browse", "").strip()
            #webbrowser.open(f"https://google.com/search?q={query}")
            return "Searching for " + query if query else "No query provided."

        elif 'play' in command:
            query = con.replace("play", "").strip()
            # open_video(f"https://www.youtube.com/results?search_query={query}")
            return f"Playing {query}"

        elif "count" in command:
            return days_remains()

        elif command in bad_word:
            return swears()

        elif 'solve' in command or 'calculate' in command or 'calculation' in command or 'solving' in command:
            t = con.replace('solve', '').replace('calculate', '').replace('calculation', '').replace('solving', '').strip()
            try:
                ans = str(eval(t))
                return ans
            except Exception:
                return "Unable to compute that expression safely."

        elif "bye" in command or "goodbye" in command or "quit" in command or "exit" in command or "q" in command:
            return "Goodbye! (web mode) — refresh the page to start again."

        elif 'monolog' in command:
            return "Work in Progress..."

        elif "open" in command:
            if "youtube" in command or "yt" in command:
                return "Opening YouTube"
            elif "instagram" in command or "insta" in command:
                return "Opening Instagram"
            elif "chatgtp" in command or "gtp" in command or "chat" in command:
                return "Opening ChatGPT"
            else:
                con = con.replace("open","Opening").strip()
                return con
            
        elif "hi" in command or "hello" in command or "hey" in command or "wassup" in command:
            return greet()
        
        else:
            return random.choice(["Sorry...", "Could you rephrase?", "I can't do that on the web."])

    # instruction stack functions (simple persistence)
    def put_file(data):
        with open("itr.txt", 'w', encoding='utf-8') as f:
            for item in data:
                f.write(encryption(item) + '\n')

    def get_file():
        data2 = []
        if not os.path.exists("itr.txt"):
            return data2
        with open("itr.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                data2.append(decryption(line.strip()))
        return data2

    last_intr = get_file()

    def inst_manager(input_str):
        if input_str not in last_intr and input_str not in ['0','1','2']:
            last_intr.append(input_str)
            if len(last_intr) > 3:
                last_intr.pop(0)
            put_file(last_intr)

    def get_inst(input_char):
        if not last_intr:
            return None
        if input_char == '0':
            return last_intr[-1]
        elif input_char == '1' and len(last_intr) > 1:
            return last_intr[1]
        elif input_char == '2' and len(last_intr) > 0:
            return last_intr[0]
        else:
            return None

    # main routing of this call
    if not user_input:
        return "I didn't receive any input."

    user_input = user_input.strip()

    if len(user_input) > 0 and user_input[0] in ['0','1','2'] and len(user_input.strip()) != 1:
        ans = generateCommand(get_inst(user_input[0]), user_input[2:])
    elif len(user_input) > 0 and user_input[0] in ['0','1','2']:
        ans = generateCommand(get_inst(user_input[0]), None)
    else:
        ans = generateCommand(user_input, None)

    # record last instruction if useful
    if ans not in ["Sorry...", "Could you rephrase?", "I can't do that on the web."] and (len(user_input) == 0 or user_input[0] not in ['0','1','2']):
        inst_manager(user_input)

    return ans if ans else "I'm Speachless..."

# =========================
# Flask routes
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api", methods=["GET","POST"])
def api():
    # accept GET /api?q=...
    if request.method == "GET":
        q = request.args.get("q","").strip()
    else:
        data = request.get_json(silent=True) or request.form
        q = (data.get("q") or data.get("message") or "").strip()

    if not q:
        return jsonify({"error":"Query missing"}), 400

    # call model
    answer = model1(q)

    # Append to chat log (like original)
    try:
        with open("chat.txt", "a", encoding='utf-8') as f:
            f.write(f"You  : {q}")
            f.write(f"\nLISA : {answer}\n")
    except Exception:
        pass

    return jsonify({"response": answer})

if __name__ == "__main__":
    # Run app
    app.run(debug=True)

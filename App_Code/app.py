# Date is 6th Dec 2025, 
# A desprate attempt to run LISA in my phone 24*7...
# Thing I do for LOVE...
# Run this "python3 ./app.py" to Start the Server.

# app.py
from flask import Flask, request, render_template, jsonify
import webbrowser
import datetime
import random
import os
import json
from datetime import date

app = Flask(__name__, static_folder="static", template_folder="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ensure_files():
    files_defaults = {
        "remind.txt": "",
        "notes.txt": "",
        "task.txt": "",
        "about.txt": "LISA 1.4 - Web assistant adapted by integration.",
        "itr.txt": "",
        "remind.json": json.dumps({
            "all_reminders": [
                {"name": "dump", "reminders": []},
                {"name": "personal", "reminders": []},
                {"name": "todo", "reminders": []},
                {"name": "business", "reminders": []}
            ]
        }, indent=4)
    }

    for fname, content in files_defaults.items():
        file_path = os.path.join(BASE_DIR, fname)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

ensure_files()
wanted = ['omit','times','all','create','monolog','gate.env','daily.env','mid.env','file','day','reminders','to','remind','me','reminder','kill','try','about','solve','solving','calculate','calculation','open','insta','instagram','yt','youtube','google','chatgtp','gtp','chat','search','browse','give','display','print','show','say','speek','task','tasks','note','notes','add', 'date', 'time', 'addn', 'addt', 'count', 'search', 'open', 'browse', 'play', 'solve', 'updates', 'hi', 'hello', 'hey', 'wassup', 'bye', 'goodbye', 'quit', 'exit', 'q', 'search', 'browse', 'google', 'delete', 'remove', 'pop', 'clear', 'wipe']
bad_word = ["mf","fuck","nigga","hoe","bitch","dog","shit","fuckyou","hundin","motherfucker","pussy","asshole"]
lastFile = "notes.txt"
repeat = 1
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
    data = {}
    with open("remind.json","r") as f:
        data = json.load(f)
    def genRemList():
        remList = []
        for i in data["all_reminders"]:
            remList.append(i["name"])
        return remList
    listRem = genRemList()
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
    def getRemList():
        ans = "Reminder Lists:\n"
        c = 0
        for i in listRem:
            ans += f"{c}. {i.capitalize()}\n"
            c+=1
        return ans.strip()
    def printRem():
        for i in data["all_reminders"]:
            c = -1
            print(i['name'].capitalize()+" Reminders:")
            for j in i['reminders']:
                print(f"{c+1}. {j}")
                c += 1
            print()
    def createRem(name):
        name = name.lower().strip()
        data["all_reminders"].append({"name":name,"reminders":[]})
        with open("remind.json","w") as f:
            json.dump(data,f, indent=4)
        listRem.append(name)
        return "Reminder by the name of "+name.capitalize()+" created."
    def addRem(name,rem):
        name = name.lower().strip()
        for i in data["all_reminders"]:
            if i["name"] == name:
                i["reminders"].append(rem)
        with open("remind.json","w") as f:
            json.dump(data,f, indent=4)
        return f"Added reminder to {name.capitalize()}."
    def emptyRem(name,rem):
        name = name.lower().strip()
        for i in data["all_reminders"]:
            if i["name"] == name:
                i["reminders"].remove(rem)
        with open("remind.json","w") as f:
            json.dump(data,f, indent=4)
    def wipeRem(name):
        name = name.lower().strip()
        for i in data["all_reminders"]:
            if i["name"] == name:
                i["reminders"] = []
        with open("remind.json","w") as f:
            json.dump(data,f, indent=4)
    def deleteRem(name):
        name = name.lower().strip()
        index = listRem.index(name)
        for i in data["all_reminders"]:
            if i["name"] == name:
                del data["all_reminders"][index]
        with open("remind.json","w") as f:
            json.dump(data,f, indent=4)
        listRem.remove(name)
    def getRem(name):
        name = name.lower().strip()
        if name not in listRem:
            return f"{name.capitalize()} is not in remidner lists."
        ans = f"{name.capitalize()} Reminders:\n"
        length = len(ans)
        for i in data["all_reminders"]:
            c = 0
            if i["name"] == str(name):
                for j in i["reminders"]:
                    ans += f"{c}. {j}"
                    ans += "\n"
                    c+=1
        if len(ans) == length:
            ans +=  "No Reminders Found."
        return ans.strip()
    def getAllRem():
        ans = ""
        for i in listRem:
            if "No Reminders Found." not in getRem(i):
                ans += getRem(i) + "\n"
                ans += '\n'

        return ans
    def removeRem(name,num):
        name = name.lower().strip()
        index = listRem.index(name)
        for i in data["all_reminders"]:
            if i["name"] == name:
                if 0 <= num > len(i["reminders"])-1:
                    return "Invalid reminder number."
                line = i["reminders"][num]
                del data["all_reminders"][index]["reminders"][num]
        with open("remind.json","w") as f:
            json.dump(data,f, indent=4)
        return f"{line} got deleted from {name.capitalize()}."

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
        x_proc = x.lower().strip().split()
        num = -1
        global repeat
        repeat = 1
        for i in x_proc:
            try:
                num = int(i)
            except Exception:
                pass
            if i.lower() in bad_word:
                return swears()
            if i in wanted and i != "" or i in listRem:
                command.append(i)
            if i == "times" or i == "time": # use 5x instead of 5 times...\
                repeat = num
        command = " ".join(command)
        print("----------------------------------------------------------------------------")
        print(f"|   The command is :    {command}\n|   The context is :    {con}\n|   The number  is :    {num}\n|   The repeat  is :    {repeat}")
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
                return addRem("dump",con)
            elif "create" in command or "new" in command or "make" in command or "divide" in command or "addn" in command:
                for i in listRem:
                    if i in command:
                        return f"Catagory of {i} already exists."
                name = con.replace("create","").replace("new","").replace("make","").replace("divide","").replace("addn","").strip()
                return createRem(name)
            elif "give" in command or "show" in command or "print" in command or "display" in command:
                if "all" in command:
                    return getAllRem()
                for i in listRem:
                    if i in command:
                        return getRem(i)
                else:
                    return "Specify which reminders to display."
            elif 'clear' in command or 'erase' in command or 'wipe' in command:
                for i in listRem:
                    if i in command:
                        return wipeRem(i)
                return "Specify which reminders to clear."
            elif "omit" in command:
                if con in listRem:
                    deleteRem(con)
                    return f"{con.capitalize()} Reminder Deleted."
                return "Specify which reminder to delete."
            elif 'remove' in command or 'delete':
                if 'all' in command:
                    for i in listRem:
                        if i in command:
                            return deleteRem(i)
                    return "Specify which reminders to delete."
                else:
                    for i in listRem:
                        if i in command:
                            if num == -1:
                                return "Specify which reminder number to remove."
                            return removeRem(i, num)
                    return "Specify which reminders to remove from."
            elif "me" in command and "to" in command:
                return addRem("dump",con)
            elif "me" in command:
                return getAllRem()
            else:
                return "What do you want to do with reminders?"

        elif 'pop' in command or 'delete' in command or 'del' in command:
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
                return decryption(open_file("notes.txt"))
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

    if not user_input:
        return "I didn't receive any input."

    user_input = user_input.strip()

    if len(user_input) > 0 and user_input[0] in ['0','1','2'] and len(user_input.strip()) != 1:
        ans = generateCommand(get_inst(user_input[0]), user_input[2:])
    elif len(user_input) > 0 and user_input[0] in ['0','1','2']:
        ans = generateCommand(get_inst(user_input[0]), None)
    else:
        ans = generateCommand(user_input, None)

    if ans not in ["Sorry...", "Could you rephrase?", "I can't do that on the web."] and (len(user_input) == 0 or user_input[0] not in ['0','1','2']):
        inst_manager(user_input)

    return (ans+'\n')*repeat if ans else "I'm Speachless..."

# =========================
# Flask routes
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api", methods=["GET","POST"])
def api():
    if request.method == "GET":
        q = request.args.get("q","").strip()
    else:
        data = request.get_json(silent=True) or request.form
        q = (data.get("q") or data.get("message") or "").strip()

    if not q:
        return jsonify({"error":"Query missing"}), 400

    answer = model1(q)

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

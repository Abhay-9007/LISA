# Date is 6th Dec 2025, 
# A desprate attempt to run LISA in my phone 24*7...
# Thing I do for LOVE...
'''
---------------- Things to add in this Code. ---------------
1. WebBrowsing is not working.
2. Content selection of limited.
3. Rreminders must be added.
4. Monolog is not working.
5. UI must be improved.
6. Language is not as is coded.
7. Make her responsis funny.
8. Update Swear Function.
9. More File added section for partition of new things.
10. Use Classes to achive more effictive answer.
11. Notes are not readable {might be encrypted.}
12. integrate this code with my new code base.
13. Try to sell if for real money...***
14. Make A file on which ChatGPT has the full access to read a nd write. {For using  versatile functoins.}{And this is soo cool}
15. Make a log reminder file to log a real crazy thing to have.
16. Money manager.
17. better version of monolog.
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
        "remind.txt": "\n[daily]:\n[week]:\n[month]:\n[other]:\n[general]:\n",
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
wanted = ['monolog','gate.env','daily.env','mid.env','file','day','weekly','monthly','normal','daily', 'week', 'month', 'other', 'general','to','remind','me','reminder','kill','try','about','solve','solving','calculate','calculation','open','insta','instagram','yt','youtube','google','chatgtp','gtp','chat','search','browse','give','display','print','show','say','speek','task','tasks','note','notes','add', 'date', 'time', 'i love you', 'addn', 'addt', 'count', 'search', 'open', 'browse', 'play', 'solve', '', 'updates', 'hi', 'hello', 'hey', 'wassup', 'bye', 'goodbye', 'see you later', 'see you', 'see you around', 'quit', 'exit', 'q', 'search', 'browse', 'google', 'delete', 'remove', 'pop', 'clear', 'wipe', 'delete all', 'remove all', 'clear all', 'wipe it']
bad_word = ["mf","fuck","nigga","hoe","bitch","dog","shit","fuck you","hundin","motherfucker"]

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
                "I won't respond to insults."]
        return random.choice(toSay)

    def days_remains():
        today = date.today()
        target = date(2026, 1, 1)
        dl = (target - today).days
        ans = f"You have {dl} days left until {target.strftime('%B %d, %Y')}."
        return ans

    # file helpers
    def open_file(file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return "File not found."

    def xxx(input_opt='general'):
        options = ['daily', 'week', 'month', 'other', 'general']
        if input_opt not in options:
            return "Invalid option. Choose from: " + ", ".join(options)

        try:
            with open("remind.txt", "r", encoding='utf-8') as f:
                textd = f.readlines()
        except Exception:
            return "No reminders file."

        if not textd:
            return "Empty reminders."

        ans_ = []
        for i in textd:
            temp = i.split(':')
            if temp[0] == "[" + input_opt + "]":
                ans_ = temp[1:]
                break

        if not ans_:
            return "No items in that section."

        f_ans = ""
        count = 0
        for i in ans_:
            f_ans += f"{count}. {i.strip()}\n"
            count+=1
        return f_ans.strip()

    def aaa(x,y):
        if x not in ['daily', 'week', 'month', 'other', 'general']:
            return "Invalid Option."
        if not y:
            return "done"

        try:
            with open("remind.txt", "r", encoding='utf-8') as f:
                remind_data = f.readlines()
        except Exception:
            return "Reminders file missing."

        updated = False
        for i in range(len(remind_data)):
            if remind_data[i].startswith("["+x+"]"):
                remind_data[i] = remind_data[i].strip() + ':'+y + "\n"
                updated = True
                break

        if not updated:
            return "Could not add; format unexpected."

        with open("remind.txt", "w", encoding='utf-8') as f:
            f.writelines(remind_data)
        return y + " added in "+ x + " section."

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
        for i in x_proc:
            try:
                num = int(i)
            except Exception:
                pass
            if i in wanted and i != "":
                command.append(i)
        command = " ".join(command)
        return process_command(command, con, num)

    def process_command(command, con, num):
        # Clear commands
        if 'clear' in command or "erase" in command:
            if 'notes' in command:
                with open("notes.txt","w",encoding='utf-8') as f:
                    f.write("")
                return "Notes cleared."
            elif 'tasks' in command or 'task' in command:
                with open("task.txt","w",encoding='utf-8') as f:
                    f.write("")
                return "Tasks cleared."
            elif 'remind' in command or 'reminder' in command:
                with open("remind.txt","w",encoding='utf-8') as f:
                    f.write("\n[daily]:\n[week]:\n[month]:\n[other]:\n[general]:\n")
                return "Reminders cleared."
            else:
                return "No specific file mentioned to clear."

        # File open
        elif 'open' in command and 'file' in command:
            return open_file(con)

        # pop/delete
        elif 'pop' in command or 'delete' in command or 'del' in command:
            # basic handling for task/notes
            target = "task.txt" if 'task' in command else ("notes.txt" if 'note' in command else None)
            if target is None:
                return "Specify tasks or notes to delete from."
            try:
                with open(target, "r", encoding='utf-8') as f:
                    data = f.readlines()
            except Exception:
                return "File not found."
            if num == -1:
                num = len(data)-1
            if 0 <= num < len(data):
                deleted = data.pop(num)
                with open(target, "w", encoding='utf-8') as f:
                    f.writelines(data)
                return f"Deleted: {deleted.strip()}"
            return "Nothing to delete."

        # reminders add
        elif 'remind' in command and 'me' in command and 'to' in command:
            aaa("other",con)
            return "Reminder added."

        elif 'add' in command:
            if 'reminder' in command or 'remind' in command:
                if 'week' in command or 'weekly' in command:
                    return aaa("week",con)
                elif 'month' in command or 'monthly' in command:
                    return aaa("month",con)
                elif 'daily' in command or 'day' in command:
                    return aaa("daily",con)
                elif 'general' in command or 'normal' in command:
                    return aaa("general",con)
                else:
                    return aaa("other",con)

            elif "tasks" in command or 'task' in command:
                with open("task.txt", "a", encoding='utf-8') as f:
                    f.write(con + "\n")
                return "Task added."
            elif 'notes' in command or 'note' in command:
                with open("notes.txt", "a", encoding='utf-8') as f:
                    f.write(encryption(con) + "\n")
                return "Note saved."
            else:
                with open("task.txt", "a", encoding='utf-8') as f:
                    f.write(con + "\n")
                return "Added."

        elif 'print' in command or 'show' in command or 'display' in command or 'give' in command:
            if 'remind' in command or 'reminder' in command:
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
                return open_file("task.txt")
            elif 'notes' in command or 'note' in command:
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
            # return a link for the client to open
            return f"Search this in your browser: https://google.com/search?q={query.replace(' ','+')}" if query else "No query provided."

        elif 'play' in command:
            query = con.replace("play", "").strip()
            return f"Play on YouTube: https://www.youtube.com/results?search_query={query.replace(' ','+')}"

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
            return "Monolog mode not supported in web UI."

        elif "open" in command:
            if "youtube" in command or "yt" in command:
                return "Open: https://www.youtube.com"
            elif "instagram" in command or "insta" in command:
                return "Open: https://instagram.com"
            elif "chatgtp" in command or "gtp" in command or "chat" in command:
                return "Open: https://chat.openai.com"
            else:
                return "Open: https://google.com"

        elif "hi" in command or "hello" in command or "hey" in command or "wassup" in command:
            return greet()

        else:
            return random.choice(["Sorry, I didn't understand that.", "Could you rephrase?", "I can't do that on the web."])

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
    if ans not in ["Oops", "Sorry", "Hell No"] and (len(user_input) == 0 or user_input[0] not in ['0','1','2']):
        inst_manager(user_input)

    return ans

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
            now = datetime.datetime.now()
            f.write(f"\nYou  : {q}")
            f.write(f"\nLISA : {answer}\n")
    except Exception:
        pass

    return jsonify({"response": answer})



if __name__ == "__main__":
    # Run app
    app.run(debug=True)

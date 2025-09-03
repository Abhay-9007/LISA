import os
import datetime
import random
import sys
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

# ----------------- Setup Flask -----------------
app = Flask(__name__)
CORS(app)

# ----------------- Setup SQLite -----------------
DB_FILE = "chatbot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Tables for tasks, notes, reminders
    c.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------- Chatbot Logic -----------------
wanted = ['solve','calculate','open','search','note','task','remind','date','time','bye','exit','hi','hello','hey']

bad_word = ["mf","fuck","nigga","hoe","bitch","dog","shit","randi","motherfucker"]

def model(text):
    text = text.lower().strip()
    
    # ----------------- Helper functions -----------------
    def get_time():
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")
    
    def get_date():
        today = datetime.date.today()
        return today.strftime("%B %d, %Y")
    
    def greet():
        greetings = ["Hello! How can I help you today?", "Hi there! What can I do for you?", "Hey! What's on your mind?"]
        return random.choice(greetings)
    
    def swears():
        responses = [
            "Please watch your language.",
            "Let's keep it clean, okay?",
            "That’s not very nice."
        ]
        return random.choice(responses)
    
    # ----------------- Commands -----------------
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if any(word in text for word in bad_word):
        return swears()
    
    if "bye" in text or "exit" in text:
        return "Goodbye! Have a great day."

    if "time" in text:
        return f"The current time is {get_time()}"
    
    if "date" in text:
        return f"Today's date is {get_date()}"
    
    if "hi" in text or "hello" in text or "hey" in text:
        return greet()

    # Notes
    if "add note" in text:
        note_content = text.replace("add note", "").strip()
        c.execute("INSERT INTO notes (content) VALUES (?)", (note_content,))
        conn.commit()
        return "Note added."

    if "show notes" in text:
        c.execute("SELECT content FROM notes")
        notes = c.fetchall()
        return "\n".join(n[0] for n in notes) if notes else "No notes yet."

    # Tasks
    if "add task" in text:
        task_content = text.replace("add task", "").strip()
        c.execute("INSERT INTO tasks (content) VALUES (?)", (task_content,))
        conn.commit()
        return "Task added."
    
    if "show tasks" in text:
        c.execute("SELECT content FROM tasks")
        tasks = c.fetchall()
        return "\n".join(t[0] for t in tasks) if tasks else "No tasks yet."

    # Reminders
    if "add reminder" in text or "remind me" in text:
        reminder_content = text.replace("add reminder", "").replace("remind me", "").strip()
        c.execute("INSERT INTO reminders (content) VALUES (?)", (reminder_content,))
        conn.commit()
        return "Reminder added."
    
    if "show reminders" in text:
        c.execute("SELECT content FROM reminders")
        reminders = c.fetchall()
        return "\n".join(r[0] for r in reminders) if reminders else "No reminders yet."

    # Solve simple math
    if "solve" in text or "calculate" in text:
        try:
            expression = text.replace("solve", "").replace("calculate", "").strip()
            answer = str(eval(expression))
            return answer
        except Exception:
            return "I couldn't solve that."

    # Default
    return "Sorry, I didn't understand that."

# ----------------- Flask Routes -----------------
@app.route("/")
def home():
    return "Chatbot API is live!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    response = model(user_input)
    return jsonify({"response": response})

# ----------------- Run Server -----------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# model.py
import webbrowser
import datetime
import random
import sys
import os
import threading
from datetime import date
import sqlite3

# Try to detect Android environment
IS_ANDROID = False
try:
    from jnius import autoclass, cast
    from android import activity
    IS_ANDROID = True
except Exception:
    IS_ANDROID = False

# Try to import TTS/speech libs for desktop fallback
try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    from gtts import gTTS
except Exception:
    gTTS = None

try:
    import pygame
except Exception:
    pygame = None

# TTS helper (Android uses Android TTS via pyjnius; desktop uses gTTS+pygame fallback)
def speak_async(text):
    def _speak(t):
        if IS_ANDROID:
            try:
                # Android TextToSpeech via Intent (use ACTION_SPEAK via TextToSpeech requires service; simpler: use android.speech.tts)
                # Use android.speech.tts.TextToSpeech via pyjnius
                TTS = autoclass('android.speech.tts.TextToSpeech')
                Locale = autoclass('java.util.Locale')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                # Initialize TTS and speak (this is a naive approach - may reinitialize each time)
                tts_obj = TTS(activity.getApplicationContext(), None)
                tts_obj.speak(t, TTS.QUEUE_FLUSH, None, "LISA_ID")
            except Exception as e:
                print("Android TTS error:", e)
        else:
            if gTTS and pygame:
                try:
                    fname = os.path.join(os.path.dirname(__file__), "response.mp3")
                    gTTS(text=t, lang='en').save(fname)
                    pygame.mixer.init()
                    pygame.mixer.music.load(fname)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pass
                    try:
                        os.remove(fname)
                    except Exception:
                        pass
                except Exception as e:
                    print("gTTS/pygame TTS error:", e)
            else:
                print("TTS:", t)
    threading.Thread(target=_speak, args=(text,), daemon=True).start()

def get_db_path():
    db_name = "assistant.db"
    try:
        if IS_ANDROID:
            from kivy.app import App
            app = App.get_running_app()
            if app:
                return os.path.join(app.user_data_dir, db_name)
    except Exception:
        pass
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)

DB_PATH = get_db_path()
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
conn.commit()

bad_word = ["mf","fuck","nigga","hoe","bitch","dog","shit","fuck you","randi","motherfucker"]

# Voice listening entrypoint. Accepts a callback function where recognized text will be delivered.
def start_listen(callback):
    if IS_ANDROID:
        try:
            # Use RecognizerIntent to prompt user speech and return result via activity.on_activity_result
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            RecognizerIntent = autoclass('android.speech.RecognizerIntent')
            Intent = autoclass('android.content.Intent')
            activity = PythonActivity.mActivity

            REQUEST_CODE = 12345
            intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak now")
            intent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)

            # Define result handler
            def _on_activity_result(request_code, result_code, intent_obj):
                try:
                    if request_code == REQUEST_CODE:
                        RESULT_OK = -1
                        if result_code == RESULT_OK and intent_obj is not None:
                            # get results
                            extras = intent_obj.getExtras()
                            if extras is not None and extras.containsKey(RecognizerIntent.EXTRA_RESULTS):
                                arr = intent_obj.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
                                if arr is not None and arr.size() > 0:
                                    txt = str(arr.get(0))
                                    callback(txt)
                                    return
                        callback("")  # no result
                except Exception as e:
                    print("on_activity_result error:", e)
                    callback("")

            # bind the python handler
            try:
                activity.bind(on_activity_result=_on_activity_result)
            except Exception as e:
                # fallback for some Kivy versions: use android.activity
                try:
                    from android import activity as android_activity
                    android_activity.bind(on_activity_result=_on_activity_result)
                except Exception as e2:
                    print("Bind error:", e, e2)

            # start intent
            activity.startActivityForResult(intent, REQUEST_CODE)
        except Exception as e:
            print("Android start_listen error:", e)
            callback("")
    else:
        # Desktop fallback: use speech_recognition to record from mic
        def _desktop_listen(cb):
            if sr is None:
                cb("")
                return
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source, timeout=6, phrase_time_limit=8)
                text = r.recognize_google(audio)
                cb(text)
            except Exception as e:
                print("Desktop listen error:", e)
                cb("")
        threading.Thread(target=_desktop_listen, args=(callback,), daemon=True).start()

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%H:%M:%S')}"

def get_date():
    today = datetime.date.today()
    return f"Today's date is {today.strftime('%B %d, %Y')}"

def exit_assistant():
    speak_async("Goodbye! Have a great day.")
    return "Goodbye! (close the app manually on Android)"

def swears():
    toSay= [
        "That's not nice.",
        "Please watch your language.",
        "I won't respond to abuse."
    ]
    return random.choice(toSay)

def days_remains():
    today = date.today()
    target = date(2026, 1, 1)
    dl = (target - today).days
    return f"You have {dl} days left."

def process_command_logic(command, con, num):
    command = command.lower()
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
    elif 'pop' in command or 'delete' in command or 'del' in command:
        cursor.execute("SELECT id, text FROM reminders")
        rows = cursor.fetchall()
        if not rows:
            return "Nothing to delete"
        if num == -1:
            num = rows[-1][0]
        cursor.execute("DELETE FROM reminders WHERE id=?", (num,))
        conn.commit()
        return f"Deleted reminder {num}"
    elif 'remind' in command and 'me' in command and 'to' in command:
        cursor.execute("INSERT INTO reminders (text) VALUES (?)", (con,))
        conn.commit()
        return "Reminder Added"
    elif 'remind' in command and 'me' in command:
        cursor.execute("SELECT text FROM reminders")
        rows = cursor.fetchall()
        return "\\n".join([r[0] for r in rows]) if rows else "No reminders"
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
    elif 'print' in command or 'show' in command or 'display' in command or 'give' in command:
        if 'reminder' in command or 'remind' in command:
            cursor.execute("SELECT text FROM reminders")
            rows = cursor.fetchall()
            return "\\n".join([r[0] for r in rows]) if rows else "No reminders"
        elif "tasks" in command or 'task' in command:
            cursor.execute("SELECT text FROM tasks")
            rows = cursor.fetchall()
            return "\\n".join([r[0] for r in rows]) if rows else "No tasks"
        elif 'notes' in command or 'note' in command:
            cursor.execute("SELECT text FROM notes")
            rows = cursor.fetchall()
            return "\\n".join([r[0] for r in rows]) if rows else "No notes"
        else:
            return "No data found"
    elif 'say' in command or 'speak' in command:
        return con
    elif 'date' in command:
        return get_date()
    elif 'time' in command:
        return get_time()
    elif 'search' in command or 'browse' in command or 'google' in command:
        query = con.strip()
        try:
            webbrowser.open(f"https://google.com/search?q={query}")
            return f"Searching for {query}"
        except Exception as e:
            return f"Failed to open browser: {e}"
    elif 'play' in command:
        query = con.strip()
        try:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return f"Playing {query} on YouTube"
        except Exception as e:
            return f"Failed to open YouTube: {e}"
    elif "count" in command:
        return days_remains()
    elif command in bad_word:
        return swears()
    elif 'solve' in command or 'calculate' in command or 'calculation' in command or 'solving' in command:
        t = con.strip().replace('solve','').replace('calculate','').replace('calculation','').replace('solving','')
        if t == '':
            return "No calculation provided"
        try:
            ans = str(eval(t, {"__builtins__": None}, {}))
            return ans
        except Exception:
            return "Error in calculation"
    elif "kill" in command or "bye" in command or "goodbye" in command or "see you later" in command or "quit" in command or "exit" in command or "q" in command:
        return exit_assistant()
    elif "open" in command:
        if "youtube" in command or "yt" in command:
            try:
                webbrowser.open("https://www.youtube.com")
                return "Opening YouTube"
            except Exception as e:
                return f"Failed: {e}"
        elif "instagram" in command or "insta" in command:
            try:
                webbrowser.open("https://instagram.com")
                return "Opening Instagram"
            except Exception as e:
                return f"Failed: {e}"
        elif "chatgtp" in command or "gtp" in command or "chat" in command:
            try:
                webbrowser.open("https://chat.openai.com")
                return "Opening ChatGPT"
            except Exception as e:
                return f"Failed: {e}"
        else:
            try:
                webbrowser.open("https://google.com")
                return "Opening Google"
            except Exception as e:
                return f"Failed: {e}"
    elif "hi" in command or "hello" in command or "hey" in command or "wassup" in command:
        greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! What's on your mind?"
        ]
        return random.choice(greetings)
    else:
        return "Oops, I don't understand."

def model(text):
    now = datetime.datetime.now()
    today = datetime.date.today()
    try:
        cursor.execute("INSERT INTO chat (role, message) VALUES (?, ?)", ("System", f"--- {today}, {now} --- LISA 2.0 ---"))
        conn.commit()
    except Exception:
        pass

    user_input = text or ""
    ans = process_command_logic(user_input.lower(), user_input, -1)

    try:
        cursor.execute("INSERT INTO chat (role, message) VALUES (?, ?)", ("You", user_input))
        cursor.execute("INSERT INTO chat (role, message) VALUES (?, ?)", ("LISA", ans))
        conn.commit()
    except Exception:
        pass

    try:
        speak_async(ans)
    except Exception:
        pass

    return ans

if __name__ == "__main__":
    print("Test:", model("give me task"))

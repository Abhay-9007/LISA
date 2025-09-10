# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TerminalTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = []
        self.history_index = -1
        self.prompt = "$ "

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Basic handling; mobile keyboards may not send 'up'/'down'
        if keycode[1] == 'enter':
            command = self.text[len(self.prompt):].strip()
            if command:
                self.history.insert(0, command)
                self.history_index = -1
                app = App.get_running_app()
                app.process_command(command)
                self.text = self.prompt
            return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

class TerminalLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(width=self.update_text_width)

    def update_text_width(self, *args):
        self.text_size = (self.width - dp(20), None)

class TerminalApp(App):
    output_text = StringProperty("LISA Terminal v2.0\\nType 'help' for available commands\\n")

    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        layout = BoxLayout(orientation='vertical', spacing=5, padding=10)

        self.output_label = TerminalLabel(
            text=self.output_text,
            size_hint_y=None,
            valign='top',
            halign='left',
            text_size=(None, None),
            color=(0.8, 0.8, 0.8, 1),
            padding_x=dp(10),
            padding_y=dp(5)
        )
        self.output_label.bind(texture_size=self.output_label.setter('size'))

        scroll = ScrollView(size_hint=(1, 1), bar_width=dp(10), scroll_type=['bars', 'content'])
        scroll.add_widget(self.output_label)
        layout.add_widget(scroll)

        # Input + buttons
        bottom = BoxLayout(size_hint_y=None, height=dp(48), spacing=6)
        self.input_field = TerminalTextInput(
            multiline=False,
            text="$ ",
            padding_x=dp(10)
        )
        voice_btn = Button(text="🎤 Voice", size_hint_x=None, width=dp(100))
        voice_btn.bind(on_release=self.on_voice)
        send_btn = Button(text="Send", size_hint_x=None, width=dp(80))
        send_btn.bind(on_release=self.on_send)

        bottom.add_widget(self.input_field)
        bottom.add_widget(voice_btn)
        bottom.add_widget(send_btn)
        layout.add_widget(bottom)

        Window.bind(size=self.on_window_size)
        return layout

    def on_window_size(self, instance, value):
        if hasattr(self, 'output_label'):
            self.output_label.text_size = (self.output_label.width - dp(20), None)

    def on_start(self):
        # import model so DB path uses App.user_data_dir
        try:
            import model  # noqa: F401
        except Exception as e:
            self.update_output(f"Error importing model: {e}\\n")
        Clock.schedule_once(self.focus_input, 0.1)

    def focus_input(self, dt):
        self.input_field.focus = True

    def on_send(self, instance):
        command = self.input_field.text[len(self.input_field.prompt):].strip() if hasattr(self.input_field, 'prompt') else self.input_field.text.strip()
        if command:
            self.input_field.text = self.input_field.prompt if hasattr(self.input_field,'prompt') else ""
            self.process_command(command)

    def on_voice(self, instance):
        self.update_output("Listening...\\n")
        # start listening via model; model.start_listen must accept a callback function
        def callback(recognized_text):
            # This will be called from background / Android callback thread; schedule to main thread
            Clock.schedule_once(lambda dt: self._handle_voice_result(recognized_text), 0)
        try:
            import model
            model.start_listen(callback)
        except Exception as e:
            self.update_output(f"Voice start error: {e}\\n")

    def _handle_voice_result(self, text):
        if not text:
            self.update_output("No voice input recognized.\\n")
            return
        # show recognized
        self.update_output(f"Recognized: {text}\\n")
        self.process_command(text)

    def process_command(self, command):
        self.update_output(f"$ {command}\\n")
        def worker(cmd):
            try:
                from model import model as run_model
                result = run_model(cmd)
            except Exception as e:
                result = f"Error: {e}"
            Clock.schedule_once(lambda dt: self.update_output(f"{result}\\n"), 0)
        threading.Thread(target=worker, args=(command,), daemon=True).start()

    def update_output(self, text):
        self.output_text += text
        self.output_label.text = self.output_text
        self.output_label.text_size = (self.output_label.width - dp(20), None)
        # Scroll to bottom
        try:
            for child in self.root.children:
                from kivy.uix.scrollview import ScrollView
                if isinstance(child, ScrollView):
                    child.scroll_y = 0
                    break
        except Exception:
            pass

if __name__ == '__main__':
    TerminalApp().run()

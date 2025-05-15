import threading
import tkinter as tk
from tkinter import scrolledtext
import re
import time

from speech_to_text import listen_from_mic
from ai_agent import ask_ai
from text_to_speech import speak_text

_think_block = re.compile(r"<think>.*?</think>", re.DOTALL)

def clean_text(text: str) -> str:
    text = re.sub(_think_block, "", text)
    text = text.replace("<think>", "").replace("</think>", "")
    return text

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("Voice Chat Agent")
        
        master.rowconfigure(0, weight=9)
        master.rowconfigure(1, weight=1)
        master.columnconfigure(0, weight=1)

        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', wrap='word')
        self.chat_area.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        control_frame = tk.Frame(master)
        control_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=(0,5))
        control_frame.columnconfigure(0, weight=1)

        self.record_button = tk.Button(control_frame, text="Record", command=self.start_listening)
        self.record_button.grid(row=0, column=0, sticky='ew')

    def append_message(self, sender: str, message: str):
        self.chat_area.config(state='normal')
        self.chat_area.insert('end', f"{sender}: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview('end')

    def insert_to_last_line(self, text: str):
        self.chat_area.config(state='normal')
        self.chat_area.insert('end', text)
        self.chat_area.config(state='disabled')
        self.chat_area.yview('end')

    def start_listening(self):
        self.record_button.config(state='disabled')
        threading.Thread(target=self._handle_conversation, daemon=True).start()

    def _handle_conversation(self):
        user_text = listen_from_mic()
        
        #user_text = "It's a me, Mario!"
        
        if not user_text:
            self._enable_button()
            return

        self.master.after(0, lambda: self.append_message("You", user_text))

        self.master.after(0, lambda: self.insert_to_last_line("AI: "))

        stream = ask_ai(user_text)
        full_reply = ""
        sentence_buffer = ""
        for chunk in stream:
            raw_content = chunk['message']['content']
            content = clean_text(raw_content)
            if not content:
                continue

            full_reply += content
            sentence_buffer += content

            self.master.after(0, lambda c=content: self.insert_to_last_line(c))

            if any(p in content for p in [".", "!", "?"]):
                to_speak = sentence_buffer.strip()
                sentence_buffer = ""
                speak_text(to_speak)
                time.sleep(0.1)
                
        if sentence_buffer.strip():
            speak_text(sentence_buffer.strip())

        self.master.after(0, lambda: self.insert_to_last_line("\n"))
        self._enable_button()


    def _enable_button(self):
        self.master.after(0, lambda: self.record_button.config(state='normal'))


def main():
    root = tk.Tk()
    root.geometry('600x400')
    app = ChatGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
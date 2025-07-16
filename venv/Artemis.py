import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import tkinter as tk
import threading
import math
import json
import os
import time

# ======================== GUI CLASS (dit gedeelte is gedaan met AI) ========================

DATA_FILE = 'artemis_memory.json'

def load_memory():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_memory(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class JarvisDisplay:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ARTEMIS")
        self.window.geometry("600x600")
        self.window.configure(bg="black")
        self.canvas = tk.Canvas(self.window, width=600, height=600, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.status_text = self.canvas.create_text(300, 550, text="System Online",
                                                   fill="cyan", font=("Consolas", 20))

        self.center_x, self.center_y = 300, 300
        self.base_radius = 60

        # Cirkel en lijnen
        self.circle = self.canvas.create_oval(self.center_x - self.base_radius,
                                              self.center_y - self.base_radius,
                                              self.center_x + self.base_radius,
                                              self.center_y + self.base_radius,
                                              outline="cyan", width=3)

        # Meerdere lijnen rondom de cirkel, start- en eindpunten per lijn
        self.lines = []
        self.num_lines = 12
        self.line_length = 30
        for i in range(self.num_lines):
            angle = 2 * math.pi * i / self.num_lines
            x0 = self.center_x + self.base_radius * math.cos(angle)
            y0 = self.center_y + self.base_radius * math.sin(angle)
            x1 = self.center_x + (self.base_radius + self.line_length) * math.cos(angle)
            y1 = self.center_y + (self.base_radius + self.line_length) * math.sin(angle)
            line = self.canvas.create_line(x0, y0, x1, y1, fill="cyan", width=2)
            self.lines.append(line)

        self.pulsing = False
        self.scale = 1.0
        self.growing = True
        self.angle_offset = 0  # voor rotatie animatie

        self.animate()

    def set_status(self, text):
        self.canvas.itemconfig(self.status_text, text=text)

    def start_pulsing(self):
        self.pulsing = True

    def stop_pulsing(self):
        self.pulsing = False
        # Reset cirkel en lijnen naar basispositie en kleur
        self.canvas.coords(self.circle,
                           self.center_x - self.base_radius,
                           self.center_y - self.base_radius,
                           self.center_x + self.base_radius,
                           self.center_y + self.base_radius)
        for i, line in enumerate(self.lines):
            angle = 2 * math.pi * i / self.num_lines
            x0 = self.center_x + self.base_radius * math.cos(angle)
            y0 = self.center_y + self.base_radius * math.sin(angle)
            x1 = self.center_x + (self.base_radius + self.line_length) * math.cos(angle)
            y1 = self.center_y + (self.base_radius + self.line_length) * math.sin(angle)
            self.canvas.coords(line, x0, y0, x1, y1)
            self.canvas.itemconfig(line, fill="cyan")

    def animate(self):
        if self.pulsing:
            # Pulsatie schaal
            if self.growing:
                self.scale += 0.05
                if self.scale >= 1.5:
                    self.growing = False
            else:
                self.scale -= 0.05
                if self.scale <= 1.0:
                    self.growing = True

            # Cirkel groter/kleiner maken
            radius = self.base_radius * self.scale
            self.canvas.coords(self.circle,
                               self.center_x - radius,
                               self.center_y - radius,
                               self.center_x + radius,
                               self.center_y + radius)

            # Lijnen rotatie en puls kleur
            self.angle_offset += 0.05
            for i, line in enumerate(self.lines):
                angle = 2 * math.pi * i / self.num_lines + self.angle_offset
                x0 = self.center_x + radius * math.cos(angle)
                y0 = self.center_y + radius * math.sin(angle)
                x1 = self.center_x + (radius + self.line_length * self.scale) * math.cos(angle)
                y1 = self.center_y + (radius + self.line_length * self.scale) * math.sin(angle)
                self.canvas.coords(line, x0, y0, x1, y1)

                # Kleuren laten pulseren in cyan tinten
                intensity = int(128 + 127 * math.sin(self.angle_offset * 10 + i))
                color = f'#00{intensity:02x}{intensity:02x}'
                self.canvas.itemconfig(line, fill=color)
        else:
            # Als niet pulsing, reset naar standaard
            self.stop_pulsing()

        self.window.after(50, self.animate)

    def close(self):
        self.window.destroy()

# ======================== ARTEMIS SETUP (vanaf hier is het weer jouw code) ========================

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

display = JarvisDisplay()

def remember(text):
    memory = load_memory()
    memory.append(text)
    save_memory(memory)
    talk("I have remembered that.")

def recall():
    memory = load_memory()
    if not memory:
        talk("I don't remember anything yet.")
    else:
        talk("Here is what I remember:")
        for item in memory[-5:]:
            talk(item)

def talk(text):
    display.set_status("Speaking...")
    display.start_pulsing()
    engine.say(text)
    engine.runAndWait()
    display.stop_pulsing()
    display.set_status("")

def take_command():
    try:
        with sr.Microphone() as source:
            display.set_status("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower().strip()

            if command.startswith("artemis"):
                command = command.replace("artemis", "", 1).strip()
                return command
            else:
                print("Wake word not detected.")
                print(command)
                display.set_status("Start your sentence with 'Artemis'")
                time.sleep(2)
                return ""
    except Exception as e:
        print("Error in take_command():", e)
        return ""

def run_artemis():
    talk("Good morning. I am Artemis. How can I assist you?")
    running = True
    while running:
        command = take_command()
        if not command:
            continue

        print(f"User: {command}")

        if command.startswith("remember"):
            to_remember = command.replace("remember", "").strip()
            if to_remember:
                remember(to_remember)
            else:
                talk("What should I remember?")
        elif "do you remember" in command or "what do you know" in command:
            recall()

        if 'play' in command:
            song = command.replace('play', '')
            talk('Playing ' + song)
            pywhatkit.playonyt(song)

        elif 'time' in command:
            time_str = datetime.datetime.now().strftime('%I:%M %p')
            talk('The time is ' + time_str)
            print(time_str)

        elif 'who is' in command:
            person = command.replace('who is', '')
            try:
                info = wikipedia.summary(person, 1)
                print(info)
                talk(info)
            except:
                talk("Sorry, I couldn't find any information.")

        elif 'what is' in command:
            thing = command.replace('what is', '')
            try:
                info = wikipedia.summary(thing, 1)
                print(info)
                talk(info)
            except:
                talk("Sorry, I couldn't find any information.")

        elif 'joke' in command:
            joke = pyjokes.get_joke("en", "chuck")
            print(joke)
            talk(joke)

        elif 'hello' in command or 'hallo' in command:
            talk('Hello, how can I help you?')

        elif 'stop' in command or 'bye' in command or 'exit' in command:
            talk('Goodbye!')
            running = False
            display.close()

        elif '' in command:
            talk('')

        else:
            talk('I did not understand. Please repeat.')

# ======================== Toegevoegde startfunctie ========================

def start_artemis():
    threading.Thread(target=run_artemis, daemon=True).start()
    display.window.mainloop()


if __name__ == "__main__":
    start_artemis()

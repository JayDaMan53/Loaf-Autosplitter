import pickle
from tkinter import Tk, Label, Entry, StringVar, Button
import pyautogui
import keyboard
import time

FilePath = "Data\\settings.pkl"
EndImgPath = "Data\\template.png"
StartImgPath = "Data\\template1.png"

print("To stop the auto splitter close this window!")

class SettingsWindow:
    def __init__(self, master):
        self.master = master
        master.title("Loaf Settings")
        master.configure(bg='darkgrey')

        self.keybind = StringVar()
        self.keybind.trace("w", self.save_settings)

        self.reset_key = StringVar()
        self.reset_key.trace("w", self.save_settings)

        self.load_settings()

        self.label1 = Label(master, text="Start/Split Keybind", font=('Arial', 14), bg='darkgrey')
        self.label1.grid(row=0, column=0, padx=20, pady=20)

        self.entry1 = Entry(master, textvariable=self.keybind, font=('Arial', 12), bg='white')
        self.entry1.grid(row=1, column=0, padx=20, pady=20)

        self.label2 = Label(master, text="Reset Keybind", font=('Arial', 14), bg='darkgrey')
        self.label2.grid(row=2, column=0, padx=20, pady=20)

        self.entry2 = Entry(master, textvariable=self.reset_key, font=('Arial', 12), bg='white')
        self.entry2.grid(row=3, column=0, padx=20, pady=20)

        self.done_button = Button(master, text="Done", command=self.on_close, bg='white', font=('Arial', 12),)
        self.done_button.grid(row=4, column=0, padx=20, pady=20)

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def save_settings(self, *args):
        settings = {"keybind": self.keybind.get(), "reset_key": self.reset_key.get()}
        with open(FilePath, "wb") as file:
            pickle.dump(settings, file)

    def load_settings(self):
        try:
            with open(FilePath, "rb") as file:
                settings = pickle.load(file)
                self.keybind.set(settings.get("keybind", ""))
                self.reset_key.set(settings.get("reset_key", ""))
        except FileNotFoundError:
            self.keybind.set("")
            self.reset_key.set("")

    def on_close(self):
        self.save_settings()
        self.master.destroy()

def load_settings():
    try:
        with open(FilePath, "rb") as file:
            settings = pickle.load(file)
            return settings
    except FileNotFoundError:
        print("Settings file not found.")
        return None

def handle_start_stop(keybind, state):
    window = pyautogui.getWindowsWithTitle('Loaf: The video game')
    if window:
        if state:
            location = pyautogui.locateOnScreen(EndImgPath)
            if location:
                pyautogui.press(keybind)
                print('Timer Stopped')
                state = False
        else:
            if any(keyboard.is_pressed(key) for key in ["a", "d", "left", "right"]):
                location = pyautogui.locateOnScreen(StartImgPath)
                if location:
                    pyautogui.press(keybind)
                    print("Timer Started")
                    state = True
    else:
        print("Window Not Found")
    return state

root = Tk()
my_gui = SettingsWindow(root)
root.mainloop()

settings = load_settings()
keybind = settings["keybind"]
reset = settings['reset_key']
print("Ready")

state = False
while True:
    if keyboard.is_pressed(reset):
        state = False
        print("Reset")
    else:
        state = handle_start_stop(keybind, state)
    time.sleep(0.1)

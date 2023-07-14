import pickle
from tkinter import Tk, Label, Entry, StringVar, W, Button

FilePath = "Data\\settings.pkl"
EndImgPath = "Data\\template.png"
StartImgPath = "Data\\template1.png"

class SettingsWindow:
    def __init__(self, master):
        self.master = master
        master.title("Loaf Settings")

        self.keybind = StringVar()
        self.keybind.trace("w", self.save_settings)

        self.reset_key = StringVar()
        self.reset_key.trace("w", self.save_settings)

        self.load_settings()

        self.label1 = Label(master, text="Start/Split Keybind")
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        self.entry1 = Entry(master, textvariable=self.keybind)
        self.entry1.grid(row=1, column=0, padx=10, pady=10)

        self.label2 = Label(master, text="Reset Keybind")
        self.label2.grid(row=2, column=0, padx=10, pady=10)

        self.entry2 = Entry(master, textvariable=self.reset_key)
        self.entry2.grid(row=3, column=0, padx=10, pady=10)

        self.done_button = Button(master, text="Done", command=self.on_close)
        self.done_button.grid(row=4, column=0, padx=10, pady=10)

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.save_settings()
        self.master.destroy()

    def save_settings(self, *args):
        settings = {"keybind": self.keybind.get(), "reset_key": self.reset_key.get()}
        with open(FilePath, "wb") as file:
            pickle.dump(settings, file)

    def load_settings(self):
        try:
            with open(FilePath, "rb") as file:
                if file.read():
                    file.seek(0)  # reset file position to the start
                    settings = pickle.load(file)
                    self.keybind.set(settings.get("keybind", ""))
                    self.reset_key.set(settings.get("reset_key", ""))
        except FileNotFoundError:
            self.keybind.set("")
            self.reset_key.set("")



root = Tk()
my_gui = SettingsWindow(root)
root.mainloop()

import pyautogui
import keyboard
import time

def load_settings():
    try:
        with open(FilePath, "rb") as file:
            if file.read():
                file.seek(0)  # reset file position to the start
                settings = pickle.load(file)
                return settings
    except FileNotFoundError:
        print("Settings file not found.")
        return None
    
settings = load_settings()
keybind = settings["keybind"]
reset = settings['reset_key']
print("Ready")
state = False

while True:
    time.sleep(0.1)  # wait for a while before each check

    if keyboard.is_pressed(reset):
        state = False
        print("Reset")

    if not state:
        if keyboard.is_pressed("left") or keyboard.is_pressed("right") or keyboard.is_pressed("a") or keyboard.is_pressed("d"):
            window = pyautogui.getWindowsWithTitle('Loaf: The video game')
        # if such a window is found
            if window:
            # check if the template image is on screen
                location = pyautogui.locateOnScreen(StartImgPath)
                if location:
                    pyautogui.press(keybind)
                    print("Timer Started")
                    state = True
            else:
                print("Window Not Found")
    else:
        # get list of windows matching 'Loaf: The video game'
        window = pyautogui.getWindowsWithTitle('Loaf: The video game')
        # if such a window is found
        if window:
            # check if the template image is on screen
            location = pyautogui.locateOnScreen(EndImgPath)
            if location:
                # if the image is found, press the key from settings
                pyautogui.press(keybind)
                print('Timer Stopped')
                state = False
        else:
                print("Window Not Found")

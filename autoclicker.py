import time
import threading
import tkinter as tk
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key


class AutoClicker:
    def __init__(self, interval):
        self.interval = interval
        self.running = False
        self.mouse = Controller()
        self.click_thread = None

    def start_clicking(self):
        self.running = True
        self.click_thread = threading.Thread(target=self.click, daemon=True)
        self.click_thread.start()

    def stop_clicking(self):
        self.running = False

    def click(self):
        while self.running:
            self.mouse.click(Button.left)
            time.sleep(self.interval)

    def on_press(self, key):
        if key == KeyCode.from_hotkey(Key.ctrl_l, Key.shift):
            if self.running:
                self.stop_clicking()
            else:
                self.start_clicking()


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("250x200")
        self.root.title("AutoClicker")

        self.interval_label = tk.Label(self.root, text="Click interval (in seconds):")
        self.interval_label.pack()

        self.interval_entry = tk.Entry(self.root)
        self.interval_entry.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_clicker)
        self.start_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        self.exit_button.pack()

        self.auto_clicker = None

    def start_clicker(self):
        interval = float(self.interval_entry.get())
        self.auto_clicker = AutoClicker(interval)
        self.auto_clicker_listener = Listener(on_press=self.auto_clicker.on_press)
        self.auto_clicker_listener.start()

        self.start_button.configure(text="Stop", command=self.stop_clicker)

    def stop_clicker(self):
        self.auto_clicker.stop_clicking()
        self.auto_clicker_listener.stop()

        self.start_button.configure(text="Start", command=self.start_clicker)

    def exit_program(self):
        self.root.destroy()


if __name__ == '__main__':
    gui = GUI()
    gui.root.mainloop()

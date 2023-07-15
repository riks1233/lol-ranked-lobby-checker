from tkinter import *
import tkinter.font as font
from threading import Thread
from checker import run_check
from logger import log


class MainButton:
    def __init__(self, root, command):
        self.root = root
        self.command = command
        self.font = font.Font(size=14)
        self.active_button = Button(
            root,
            font=self.font,
            text="Check ranked lobby",
            activebackground="lime green",
            background="lime green",
            command=self.press,
        )
        self.active_button.pack(expand=True, fill="both")
        self.working_button = Button(
            root,
            font=self.font,
            text="Checking ...",
            state="disabled",
        )

    def press_thread(self):
        log("Checking ...")
        self.active_button.pack_forget()
        self.working_button.pack(expand=True, fill="both")

        self.command()

        self.working_button.pack_forget()
        self.active_button.pack(expand=True, fill="both")
        log("Check completed.")

    def press(self):
        t = Thread(target=self.press_thread)
        t.start()


def ui_main():
    root = Tk()
    width = 400
    height = 200
    root.geometry(str(width) + "x" + str(height))
    title = "League of legends ranked lobby checker"
    root.title(title)

    main_button = MainButton(root, run_check)
    # This will run the mainloop
    # (if it wasn't in a separate thread the code below would not execute until the window is shut down).
    root.mainloop()


def init():
    # [IMPORTANT]: Someone said that tkinter is considered as non-thread-safe.
    # https://stackoverflow.com/questions/44637473/python3-tkinter-display-message-after-process-completion
    # Hence, if there would be problems, remove the threading for the UI and remove any code
    # that is supposed to run after the ui.init().
    # (For example, a message saying "Initialized successfully.")
    t = Thread(target=ui_main)
    t.start()

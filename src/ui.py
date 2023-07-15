from tkinter import *
from threading import Thread
from checker import run_check
from logger import log


class MainButton:
    def __init__(self, root, command):
        self.root = root
        self.command = command
        self.active_button = Button(
            root,
            text="Check ranked lobby",
            activebackground="lime green",
            background="lime green",
            command=self.press,
        )
        self.active_button.pack(expand=True, fill="both")
        self.working_button = Button(
            root,
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


def init():
    root = Tk()
    width = 400
    height = 200
    root.geometry(str(width) + "x" + str(height))

    # Providing title to the form
    title = "League of legends ranked lobby checker"
    root.title(title)

    main_button = MainButton(root, run_check)

    # this will run the mainloop (code below does not execute until the window is shut down).
    root.mainloop()

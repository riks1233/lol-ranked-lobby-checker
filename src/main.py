import globals
import ui
from logger import *


def main():
    globals.init()
    ui.init()
    log("Initialized successfully.")


if __name__ == "__main__":
    main()

from datetime import datetime


def log(msg=""):
    if msg == "":
        print()
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    print("[" + now + "]", msg)

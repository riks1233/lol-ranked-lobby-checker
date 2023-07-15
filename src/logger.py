from datetime import datetime


def log(msg="", level="[INFO]"):
    if msg == "" and level == "[INFO]":
        print()
        return
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    print(f"[{now}]{level}:", msg)


def log_error(msg="", e=Exception(), level="[ERROR]"):
    composed_msg = ""
    composed_msg += msg
    if (str(e)) != "":
        if composed_msg != "":
            composed_msg += " "
        composed_msg += f"Exception message: {str(e)}"

    log(composed_msg, level)


def log_warning(msg="", e=Exception()):
    log_error(msg, e, "[WARNING]")


def log_debug(msg=""):
    log(msg, "[DEBUG]")

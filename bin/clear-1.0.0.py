author = "longtrinh2666"
import os, platform

def register(commands, name="clear"):
    def clear_command(args):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    commands["clear"] = clear_command
    commands["cls"] = clear_command

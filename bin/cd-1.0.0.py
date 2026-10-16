author = "longtrinh2666"
import os

def register(commands, name="cd"):
    def cd_command(args):
        if not args:
            print(os.getcwd())
        else:
            path_2 = args[0]
            try:
                os.chdir(path_2)
                print("Changed directory to:", os.getcwd())
            except FileNotFoundError:
                print("E: The system cannot find the path specified.")
            except OSError:
                print("E: Invalid path syntax")

    commands["cd"] = cd_command

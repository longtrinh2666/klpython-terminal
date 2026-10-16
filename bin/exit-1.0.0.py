author = "longtrinh2666"
import sys

def register(commands, name="exit"):
    def exit_command(args):
        print("Exiting shell")
        sys.exit(0)

    commands["exit"] = exit_command

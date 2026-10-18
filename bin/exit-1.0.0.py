author = "longtrinh2666"
version = "1.0.0"
import sys

def register(commands, name="exit"):
    def exit_command(args):
        print("Exiting shell")
        sys.exit(0)

    commands["exit"] = exit_command

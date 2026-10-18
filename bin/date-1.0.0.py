author = "longtrinh2666"
version = "1.0.0"
import datetime

def register(commands, name="date"):
    def date_command(args):
        now = datetime.datetime.now()
        print(f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')} ")

    commands["date"] = date_command
    commands["time"] = date_command

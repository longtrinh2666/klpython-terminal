author = "longtrinh2666"
import os

def register(commands, name="type"):
    def type_command(args):
        if not args:
            print("Usage: type <filename>")
            return

        file_to_read = args[0]
        try:
            with open(file_to_read, "r", encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("E: File not found")
        except Exception as e:
            print("E: Error reading file:", e)

    commands["type"] = type_command

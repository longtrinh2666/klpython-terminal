author = "longtrinh2666"
import os

def register(commands, ENV, name="export"):
    def export_cmd(args):
        if not args or "=" not in args[0]:
            print("Usage: export VAR=value")
            return
        key, value = args[0].split("=", 1)
        os.environ[key] = value
        ENV[key] = value
        print(f"Exported {key}={value}")
    commands[name] = export_cmd


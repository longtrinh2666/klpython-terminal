author = "longtrinh2666"
import time

def register(commands, ENV):
    def sleep_cmd(args):
        if not args:
            print("Usage: sleep <seconds>")
            return

        try:
            sec = float(args[0])
            time.sleep(sec)
        except ValueError:
            print("E: Invalid seconds format")
        except KeyboardInterrupt:
            print("\nSleep interrupted")

    commands["sleep"] = sleep_cmd
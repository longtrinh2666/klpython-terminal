author = "longtrinh2666"
import os

def register(commands, ENV):
    def read_cmd(args):
        if not args:
            print("Usage: read <filename>")
            return

        target_file = args[0]
        curr_dir = ENV.get("current_dir", os.getcwd())
        file_path = os.path.abspath(os.path.join(curr_dir, target_file))

        if not os.path.exists(file_path):
            print(f"E: File not found '{target_file}'")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e:
            print("E: Cannot read file:", e)

    commands["read"] = read_cmd
    commands["cat"] = read_cmd
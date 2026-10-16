author = "longtrinh2666"
import os

def register(commands, name="mkdir"):
    def mkdir_command(args):
        if args:  # kiểm tra có tham số không
            new_folder = args[0]
            try:
                os.mkdir(new_folder)
                print("Folder created successfully ✅")
            except FileExistsError:
                print("E: Folder already exists")
            except FileNotFoundError:
                print("E: Invalid path")
            except Exception as e:
                print("E:", e)
        else:
            print("Usage: mkdir <foldername>")

    commands["mkdir"] = mkdir_command

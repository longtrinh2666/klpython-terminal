author = "longtrinh2666"
version = "1.0.0"
import shutil

def register(commands, name="copy"):
    def copy_command(args):
        if not args or len(args) < 2:
            print("Usage: copy <src> <dst> | copy -f <src> <dst>")
            return

        if args[0] == "-f":
            if len(args) < 3:
                print("Usage: copy -f <src> <dst>")
                return
            src, dst = args[1], args[2]
            try:
                shutil.copytree(src, dst)
                print("Folder copied successfully ✅")
            except FileExistsError:
                print("E: The destination folder already exists.")
            except FileNotFoundError:
                print("E: The source folder cannot be found.")
            except Exception as e:
                print("E:", e)
        else:
            src, dst = args[0], args[1]
            try:
                shutil.copy(src, dst)
                print("File copied successfully ✅")
            except FileNotFoundError:
                print("E: The source file cannot be found.")
            except Exception as e:
                print("E:", e)

    commands["copy"] = copy_command
    commands["cp"] = copy_command

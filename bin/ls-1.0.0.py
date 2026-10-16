author = "longtrinh2666"
import os, time

def register(commands, name="ls"):
    def ls_command(args):
        path = args[0] if args else os.getcwd()
        print(f"\nDirectory of {path}\n")
        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                stats = os.stat(full_path)
                size = stats.st_size
                mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats.st_mtime))

                if os.path.isdir(full_path):
                    print(f"[Folder] {item:30} {mtime}")
                else:
                    print(f"{item:30} {size:10} bytes {mtime}")
        except FileNotFoundError:
            print("E: Path not found")
        except PermissionError:
            print("E: Permission denied")

    commands["ls"] = ls_command
    commands["dir"] = ls_command

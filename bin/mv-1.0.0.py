author = "longtrinh2666"
import os

def register(commands, name="mv"):
    def mv_command(args):
        if not args or len(args) < 2:
            print("Usage: mv <old_name> <new_name>")
            print("       mv -r <old_folder> <new_folder>")
            return

        # Nếu có cờ -r thì chỉ cho phép di chuyển thư mục
        if args[0] == "-r":
            if len(args) < 3:
                print("Usage: mv -r <old_folder> <new_folder>")
                return
            old_name, new_name = args[1], args[2]
            if not os.path.isdir(old_name):
                print(f"E: '{old_name}' is not a folder.")
                return
            try:
                os.rename(old_name, new_name)
                print("The folder has been renamed or moved successfully ✅")
            except FileNotFoundError:
                print("E: The system cannot find the folder specified.")
            except Exception as e:
                print("E:", e)
        else:
            # Di chuyển file hoặc thư mục bình thường
            old_name, new_name = args[0], args[1]
            try:
                os.rename(old_name, new_name)
                print("The file/folder has been renamed or moved successfully ✅")
            except FileNotFoundError:
                print("E: The system cannot find the file specified.")
            except Exception as e:
                print("E: Error changing name:", e)

    # đăng ký cả mv và rename
    commands["mv"] = mv_command
    commands["rename"] = mv_command


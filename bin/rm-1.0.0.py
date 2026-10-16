author = "longtrinh2666"
import shutil, os

def register(commands, name="rm"):
    def rm_command(args):
        if not args:
            print("Usage: rm [-r|-rf] <folder> | rm <file>")
            return

        # Xóa thư mục không cần xác nhận (-rf)
        if args[0] == "-rf":
            if len(args) < 2:
                print("Usage: rm -rf <folder>")
                return
            folder_to_remove = args[1]
            try:
                shutil.rmtree(folder_to_remove)
                print("Folder deleted successfully ✅")
            except FileNotFoundError:
                print("E: The system cannot find the folder specified.")
            except Exception as e:
                print("E:", e)
            return

        # Xóa thư mục có xác nhận (-r)
        if args[0] == "-r":
            if len(args) < 2:
                print("Usage: rm -r <folder>")
                return
            folder_to_remove = args[1]
            confirm = input(f"Are you sure you want to delete folder '{folder_to_remove}'? (y/n) ").lower()
            if confirm == "y":
                try:
                    shutil.rmtree(folder_to_remove)
                    print("Folder deleted successfully ✅")
                except FileNotFoundError:
                    print("E: The system cannot find the folder specified.")
                except Exception as e:
                    print("E:", e)
            else:
                print("Canceled")
            return

        # Xóa file
        file_to_remove = args[0]
        confirm = input(f"Are you sure you want to delete file '{file_to_remove}'? (y/n) ").lower()
        if confirm == "y":
            try:
                os.remove(file_to_remove)
                print("File deleted successfully ✅")
            except FileNotFoundError:
                print("E: The system cannot find the file specified.")
            except IsADirectoryError:
                print("E: '{file_to_remove}' is a directory. Use rm -r or rm -rf.")
            except Exception as e:
                print("E:", e)
        else:
            print("Canceled")

    commands["rm"] = rm_command

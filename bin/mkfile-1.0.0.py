author = "longtrinh2666"
version = "1.0.0"
import os

def register(commands, ENV):
    def mkfile(args):
        """
        Create a new empty file.
        Usage: mkfile <filename>
        """
        if not args:
            print("Usage: mkfile <filename>")
            return

        target_file = args[0]
        curr_dir = os.getcwd()  # Lấy thư mục hiện tại của terminal
        
        if os.path.isabs(target_file):
            file_path = target_file
        else:
            file_path = os.path.abspath(os.path.join(curr_dir, target_file))

        if os.path.exists(file_path):
            print(f"E: File '{target_file}' already exists")
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                pass  # Tạo file rỗng
            print(f"File created: {target_file}")
        except Exception as e:
            print(f"E: Cannot create file: {e}")

    commands["mkfile"] = mkfile
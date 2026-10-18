author = "longtrinh2666"
version = "1.0.0"
import os

def register(commands, ENV):
    def cat_cmd(args):
        """
        Print file content to the screen.
        Usage: cat <filename>
        """
        if not args:
            print("Usage: cat <filename>")
            return

        target_file = args[0]
        curr_dir = os.getcwd()
        
        # Xử lý đường dẫn linh hoạt (hỗ trợ cả đường dẫn tuyệt đối lẫn tương đối)
        if os.path.isabs(target_file):
            file_path = target_file
        else:
            file_path = os.path.abspath(os.path.join(curr_dir, target_file))

        if not os.path.exists(file_path):
            print(f"E: File not found '{target_file}' (Checked in: {curr_dir})")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e:
            print("E: Cannot cat file:", e)

    commands["cat"] = cat_cmd
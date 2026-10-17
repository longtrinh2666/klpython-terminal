author = "longtrinh2666"
import os

def register(commands, ENV):
    def grep_cmd(args):
        """
        Search for a pattern/keyword inside a file.
        Usage: grep <pattern> <filename>
        """
        if len(args) < 2:
            print("Usage: grep <pattern> <filename>")
            return

        pattern = args[0]
        target_file = args[1]
        
        curr_dir = ENV.get("current_dir", os.getcwd())
        file_path = os.path.abspath(os.path.join(curr_dir, target_file))

        if not os.path.exists(file_path):
            print(f"E: File not found '{target_file}'")
            return

        try:
            matched_lines = 0
            with open(file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    if pattern in line:
                        # In ra số dòng và nội dung chứa từ khóa (có loại bỏ khoảng trắng thừa ở đuôi dòng)
                        print(f"{line_num}: {line.rstrip()}")
                        matched_lines += 1
            
            if matched_lines == 0:
                print(f"No match found for pattern '{pattern}' in '{target_file}'")
                
        except Exception as e:
            print(f"E: Cannot read file: {e}")

    # Đăng ký lệnh 'grep' vào hệ thống commands của terminal
    commands["grep"] = grep_cmd
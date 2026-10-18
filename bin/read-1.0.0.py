author = "longtrinh2666"
version = "1.0.0"
import os

def register(commands, ENV):
    def read_command(args):
        prompt = ""
        target_vars = []
        
        # Phân tích tham số truyền vào
        i = 0
        while i < len(args):
            if args[i] == "-p" and i + 1 < len(args):
                prompt = args[i + 1]
                i += 2
            else:
                target_vars.append(args[i])
                i += 1

        # Nếu không truyền tên biến, mặc định lưu vào biến "REPLY"
        if not target_vars:
            target_vars = ["REPLY"]

        try:
            # Đọc dữ liệu từ người dùng với chuỗi nhắc nhở (nếu có)
            user_input = input(prompt)
            
            # Tách các giá trị theo khoảng trắng để gán vào danh sách biến
            values = user_input.split()
            
            for idx, var_name in enumerate(target_vars):
                if idx < len(values):
                    if idx == len(target_vars) - 1:
                        # Biến cuối cùng nhận toàn bộ phần chuỗi dư còn lại
                        ENV[var_name] = " ".join(values[idx:])
                    else:
                        ENV[var_name] = values[idx]
                else:
                    ENV[var_name] = ""
                    
        except (KeyboardInterrupt, EOFError):
            print() # Xuống dòng an toàn khi user bấm Ctrl+C

    # Đăng ký lệnh vào hệ thống commands của terminal
    commands["read"] = read_command
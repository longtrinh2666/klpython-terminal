author = "longtrinh2666"

def cmd_read(args, env):
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

    # Nếu không truyền tên biến, mặc định lưu vào biến "REPLY" (giống bash)
    if not target_vars:
        target_vars = ["REPLY"]

    try:
        # Đọc dữ liệu từ người dùng
        user_input = input(prompt)
        
        # Nếu nhập nhiều biến (cách nhau bởi khoảng trắng), tách chuỗi gán lần lượt
        values = user_input.split()
        
        for idx, var_name in enumerate(target_vars):
            if idx < len(values):
                # Nếu đủ giá trị để gán cho từng biến
                if idx == len(target_vars) - 1:
                    # Biến cuối cùng nhận phần dữ liệu còn lại (nếu có khoảng trắng ở đuôi)
                    env[var_name] = " ".join(values[idx:])
                else:
                    env[var_name] = values[idx]
            else:
                # Nếu người dùng nhập thiếu, gán chuỗi rỗng
                env[var_name] = ""
                
    except (KeyboardInterrupt, EOFError):
        print() # Xuống dòng nếu user bấm Ctrl+C / Ctrl+D

# Đăng ký lệnh vào từ điển commands của terminal
commands["read"] = cmd_read
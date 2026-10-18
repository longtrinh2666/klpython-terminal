author = "longtrinh2666"
version = "1.0.0"
import os

def register(commands, ENV):
    def pwd_cmd(args):
        # Lấy thư mục hiện tại từ ENV, nếu không có thì fallback về os.getcwd()
        curr_dir = ENV.get("current_dir", os.getcwd())
        print(curr_dir)

    # Đăng ký lệnh 'pwd' vào hệ thống commands của terminal
    commands["pwd"] = pwd_cmd
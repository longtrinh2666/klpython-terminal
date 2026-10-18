author = "longtrinh2666"
version = "1.0.0"
import os

def register(commands, ENV):
    def pwd_cmd(args):
        # Lấy trực tiếp từ os.getcwd() để luôn đồng bộ tuyệt đối với thực tế os.chdir()
        print(os.getcwd())

    # Đăng ký lệnh 'pwd' vào hệ thống commands của terminal
    commands["pwd"] = pwd_cmd
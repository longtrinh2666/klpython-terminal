def register(commands, plugin_name):
    def hello(args):
        print("Hello from sandbox plugin!")
    # đăng ký lệnh theo namespace để tránh trùng
    commands[f"hello"] = hello

description = "Hello demo plugin"
version = "1.0.0"
author = "guest"
# không có plugin_key → chạy sandbox

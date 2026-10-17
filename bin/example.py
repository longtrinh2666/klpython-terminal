def register(commands, plugin_name):
    def hello(args):
        print("Hello from sandbox plugin!")
    # đăng ký lệnh theo namespace để tránh trùng
    commands[f"hello"] = hello

plugin_description = "Hello demo plugin"
plugin_version = "1.0.0"
plugin_author = "guest"
# không có plugin_key → chạy sandbox

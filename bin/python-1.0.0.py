author = "longtrinh2666"
import code

def register(commands, name="python"):
    def python_command(args):
        print("Entering Python interactive mode (type exit() or Ctrl+D to quit)")
        # mở interactive console với toàn bộ biến hiện tại
        code.interact(local=dict(globals(), **locals()))

    commands["python"] = python_command

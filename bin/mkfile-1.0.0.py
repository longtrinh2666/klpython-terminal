author = "longtrinh2666"

def register(commands, ENV, name="mkfile"):
    def mkfile(args):
        if not args:
            print("Usage: mkfile <filename>")
            return
        filename = args[0]

        if os.path.exists(filename):
            print(f"File '{filename}' already exists")
            return

        try:
            with open(filename, "w") as f:
                pass
            print(f"File '{filename}' created")
        except Exception as e:
            print("Error creating file:", e)

    commands[name] = mkfile

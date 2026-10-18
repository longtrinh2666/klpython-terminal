author = "longtrinh2666"
version = "1.0.0"
def register(commands, ENV):
    def version_command(args):
        print(f"ver: {ENV['ver']}")
    commands["version"] = version_command
    commands["ver"] = version_command

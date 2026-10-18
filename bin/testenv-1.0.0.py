author = "longtrinh2666"
version = "1.0.0"
import env

def register(commands, ENV):
    def testenv(args):
        env.test()

    commands["testenv"] = testenv

author = "longtrinh2666"
import env

def register(commands, ENV):
    def testenv(args):
        env.test()

    commands["testenv"] = testenv

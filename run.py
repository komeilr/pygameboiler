import sys
from gameengine import GameEngine


def main(args):
    print(args)
    debug = False
    console_debug = False
    if args:
        if args[0] == '1':
            console_debug = True
    
    app = GameEngine(console_debug, debug)

    app.run()


if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit()

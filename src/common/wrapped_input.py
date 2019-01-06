import sys

def wraped_input(x = ''):
    try:
        return input(x)
    except KeyboardInterrupt:
        sys.exit(0)
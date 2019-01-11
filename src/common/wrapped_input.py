import sys

def wrapped_input(x = ''):
    try:
        return input(x)
    except KeyboardInterrupt:
        sys.exit(0)
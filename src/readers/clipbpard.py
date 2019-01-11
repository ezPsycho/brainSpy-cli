import re
import sys
import time
from tkinter import Tk

class ClipboardReader:
    def __init__(self):
        self.loop = False
    
    def run(x, parser, args = None):
        # Read content from clipboard with Tk:
        root = Tk()
        root.withdraw()
        time.sleep(0.1)

        try:
            clipboard_content = root.clipboard_get()
        except:
            print('[ERROR] failed to get content from the clipboard.')
            sys.exit(1)
        
        root.destroy()

        clipboard_rows = re.split(r'[~\r\n]+', clipboard_content)

        list(map(parser.add, clipboard_rows))
import re
import sys
import time
import pyperclip

class Reader:
    def __init__(self, args):
        self.loop = False
    
    def run(self, parser):
        try:
            clipboard_content = pyperclip.paste()
        except:
            print('[ERROR] failed to get content from the clipboard.')
            sys.exit(1)

        clipboard_rows = re.split(r'[~\r\n]+', clipboard_content)

        list(map(parser.add, clipboard_rows))
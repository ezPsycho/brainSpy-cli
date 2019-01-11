import re
import sys
from os import path
from glob import glob

class Reader:
    def __init__(self, args):
        self.loop = False
        self.args = args

    def run(self, parser):
        matched_files = glob(self.args.input)

        if len(matched_files) == 0:
            print('[ERROR] The path didn\'t matched any file.')
            sys.exit(1)
        
        for _file in matched_files:
            with open(_file, 'r') as f:
                file_rows = re.split(r'[~\r\n]+',  f.read())

                if len(matched_files) == 1:
                    list(map(parser.add, file_rows))
                else:
                    batch_name = path.splitext(path.basename(_file))[0]
                    list(map(lambda x:parser.add(x, batch = batch_name), file_rows))

                return True
import re
from os import path

def fileReader(x, parser, src = None):
    if not path.isfile(src):
        print('[ERROR] %s does not exists.' % src)
        return False

    with open(file, 'r') as f:
        file_rows = re.split(r'[~\r\n]+',  f.read())

        list(map(parser.add, file_rows))

        return True
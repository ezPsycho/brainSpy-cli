import pyperclip
from tabulate import tabulate
from ..common import clean_screen

def clipboardProducer(parser, dest = None):
    parsed_tsv = parser.parse_tsv()
    pyperclip.copy(parsed_tsv)
    return True
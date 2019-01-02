from tabulate import tabulate
from ..common import clean_screen

def cliProducer(parser, dest = None):
    clean_screen()
    print('\n' + parser.parse_cli() + '\n')
    return True
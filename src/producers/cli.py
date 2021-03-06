import sys
sys.path.append('..')

from tabulate import tabulate
from common.clean_screen import clean_screen
from common.wrapped_input import wrapped_input

class Producer:
    def __init__(self, args):
        self.format = 'c'
        self.simp = False
    
    def run(self, x):
        clean_screen()
        if len(x) == 0:
            print('[INFO] Got nothing from the source.')
        else:
            print('\n' + tabulate(x, headers='keys') + '\n')

        wrapped_input('Press anykey to continue...')
        return True
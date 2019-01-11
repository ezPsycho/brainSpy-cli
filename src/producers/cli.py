from tabulate import tabulate
from ..common import clean_screen

class CliProducer:
    def __init__(self):
        self.format = 'c'
        self.simp = False
    
    def run(self, x):
        clean_screen()
        print('\n' + tabulate(x, headers='keys') + '\n')
        return True
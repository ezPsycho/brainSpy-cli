import sys
sys.path.append('..')

import csv
import pyperclip

from common import clean_screen

class Producer:
    def __init__(self):
        self.format = 'r'
        self.simp = True
    
    def run(self, x):
        parsed_tsv = csv.DictWriter() # Write Here
        pyperclip.copy(parsed_tsv)
        return True
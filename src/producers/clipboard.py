import sys
sys.path.append('..')

import csv
import pyperclip

from io import StringIO

from common import clean_screen

class Producer:
    def __init__(self, args):
        self.format = 'r'
        self.simp = True
    
    def run(self, x):
        output = StringIO()
        
        writer = csv.DictWriter(
            output, 
            fieldnames = list(x[0].keys()),
            delimiter = '\t'
        )

        writer.writeheader()
        list(map(writer.writerow, x))
        pyperclip.copy(output.getvalue())
        return True
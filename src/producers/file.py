import sys
sys.path.append('..')

import csv

from common import clean_screen

class Producer:
    def __init__(self, args):
        self.format = 'r'
        self.simp = True

        self.file = args.output
    
    def run(self, x):
        with open(self.file, 'w', newline='') as f:
            if not f.writable:
                print('[ERROR] Failed to write.')
                sys.exit(1)
            
            writer = csv.DictWriter(
                f,
                fieldnames = list(x[0].keys()),
                delimiter = '\t'
            )

            writer.writeheader()
            list(map(writer.writerow, x))

            return True
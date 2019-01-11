import os
import sys
import csv
from ..common import clean_screen

class FileProducer:
    def __init__(self, file):
        self.format = 'r'
        self.simp = True

        if not os.access(file, os.W_OK):
            print('[ERROR] Target file is not writable.')
            sys.exit(1)

        self.file = file
    
    def run(self, x):
        with open(self.file, 'w') as f:
            if not f.writable:
                print('[ERROR] Failed to write.')
                sys.exit(1)
            
            f.write(csv.DictWriter()) #Change Here

            return True
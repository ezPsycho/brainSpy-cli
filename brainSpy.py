__VERSION__ = '0.0.1'

import argparse

parser = argparse.ArgumentParser(
    description='Transform MNI coordinate to AAL and BA structural names.'
)
parser.add_argument(
    'parser', nargs='?', type=str, default='raw', 
    help='selecting one parser for different types of text'
)
parser.add_argument(
    '-r', '--radius', nargs='?', type=int, metavar='radius', dest='radius', default=None,
    help='the radius of fuzzy query, if provided, brainSpy will not only query the coordinate, but also voxels around the coordinate'
)
parser.add_argument(
    '-t', '--threshold', nargs='?', type=float, metavar='threshold', dest='threshold', default=0,
    help='the threshold of fuzzy query, incorporate unlabeled voxels from specific anatomical structures into data queries, default value is 0'
)
parser.add_argument(
    '-a', '--all-peaks', dest='all_peaks', action='store_true',
    help='for spm parser only, if keep all peaks or first peak of all clusters'
)

parser.add_argument(
    '-d', '--debug', dest='debug', action='store_true',
    help='enable debug mode, will throw error while failed to parse the content'
)

args = parser.parse_args()

import sys

sys.path.append('./modules/brainspy')

import os
import re
import time
import signal
import pyperclip
from tkinter import Tk
from tabulate import tabulate

from parsers import raw, spm

if sys.platform == 'win32':
     import pyreadline.rlmain

import readline

from brainspy import query_brain, query_names, ba_labels, aal_labels, validate_range

failed_parse_msg = '[ERROR] Failed to parse your content, please check the format.'

if args.parser not in ['raw', 'spm']:
    print('[ERROR] Parser not found, only "raw" and "spm" allowed.')
    sys.exit(1)

parsers = {
    'spm': spm.SpmParser,
    'raw': raw.RawParser
}

def silent_run(x, message):
    if args.debug:
        return x()
    else:
        try:
            return x()
        except:
            print(message)
            return False

if args.clipboard:
    _parser = parsers[args.parser](vars(args))


def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def cleanScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

cleanScreen()
terminal_marks = ['***', '****']

while True:
    cleanScreen()
    print("""
 _ __                   __,            
( /  )         o       (               
 /--< _   __, ,  _ _    `.   ,_   __  ,
/___// (_(_/(_(_/ / /_(___)_/|_)_/ (_/_
                            /|      /  
Interactive shell          (/      '   

==========================================
    """)
    last_input = ''
    _parser = parsers[args.parser](vars(args))
    
    while last_input not in terminal_marks:
        last_input = input()

        if last_input in terminal_marks:
            print('[INFO] Querying, please wait...')
            continue

        _parser.add(last_input)

    _parser.parse()

    if last_input == '****':
        pyperclip.copy(_parser.parse_clipboard())

    cleanScreen()
    print('\n' + _parser.parse_cli() + '\n')

    if not args.radius is None:
      print('* Query radius is %s, threshold is %s.' % (args.radius, args.threshold))
    
    input('\n\nPress enter to continue, Press Ctrl-C to exit.')
__VERSION__ = '0.0.2'

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
    '-c', '--clipboard', dest='clipboard', action='store_true',
    help='read content from clipboard, transform it and send the result to clipboard at once'
)

parser.add_argument(
    '-d', '--debug', dest='debug', action='store_true',
    help='enable debug mode, will throw error while failed to parse the content'
)

args = parser.parse_args()

import os
import re
import sys
import time
import pyperclip
from tkinter import Tk
from tabulate import tabulate

from parsers import raw, spm

if sys.platform == 'win32':
     import pyreadline.rlmain

import readline

from modules.brainspy.brainspy import query_brain, query_names, ba_labels, aal_labels, validate_range

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

    root = Tk()
    root.withdraw()
    time.sleep(0.1)

    try:
        clipboard_content = root.clipboard_get()
    except:
        print('[ERROR] failed to get content from the clipboard.')
        sys.exit(1)
    
    root.destroy()

    clipboard_rows = re.split(r'[~\r\n]+', clipboard_content)

    list(map(_parser.add, clipboard_rows))
    result = silent_run(_parser.parse, failed_parse_msg)
    
    if result is False:
        sys.exit(1)

    parsed_tsv = silent_run(_parser.parse_tsv, failed_parse_msg)
    pyperclip.copy(parsed_tsv)

    sys.exit(0)

readline.parse_and_bind("set disable-completion on")  
readline.parse_and_bind("tab: self-insert")

def signal_handler(sig, frame):
    sys.exit(0)

def cleanScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wraped_input(x = ''):
    try:
        return input(x)
    except KeyboardInterrupt:
        sys.exit(0)

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
        last_input = wraped_input()

        if last_input in terminal_marks:
            print('[INFO] Querying, please wait...')
            continue

        _parser.add(last_input)

    result = silent_run(_parser.parse, failed_parse_msg)

    if result is False:
        continue

    if last_input == '****':
        parsed_tsv = silent_run(_parser.parse_tsv, failed_parse_msg)
        pyperclip.copy(parsed_tsv)

    cleanScreen()
    print('\n' + _parser.parse_cli() + '\n')

    if not args.radius is None:
      print('* Query radius is %s, threshold is %s.' % (args.radius, args.threshold))
    
    wraped_input('\n\nPress enter to continue, Press Ctrl-C to exit.')
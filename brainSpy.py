import argparse

parser = argparse.ArgumentParser(
    description='Transform MNI coordinate to AAL and BA structural names.')
parser.add_argument(
    '-r', '--radius', nargs=1, type=int, metavar='radius', dest='radius', default=[None, ],
    help='the radius of fuzzy query, if provided, brainSpy will not only query the coordinate, but also voxels around the coordinate'
)
parser.add_argument(
    '-t', '--threshold', nargs=1, type=float, metavar='threshold', dest='threshold', default=[0, ],
    help='the threshold of fuzzy query, incorporate unlabeled voxels from specific anatomical structures into data queries, default value is 0'
)

args = parser.parse_args()

import os
import re
import sys
import signal

from tabulate import tabulate
from modules.brainspy.brainspy import query_brain, query_names, ba_labels, aal_labels, validate_range

regex = r'[\d+\-]+'

def signal_handler(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def cleanScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def filterInputs(x):
    c = re.findall(regex, x)
    if len(c) < 3:
        return None
    else:
        return list(map(lambda x: round(float(x)), c[0:3]))


def _to_str_list(x):
    return list(map(str, x))


def _query_brain(x):
    if not x is None:
        result = query_brain(*x, args.radius[0], args.threshold[0])

        aal_labels = '\n'.join(_to_str_list([result[3]] + result[8]))
        ba_idxs = '\n'.join(_to_str_list([result[5]] + result[9]))
        ba_labels = '\n'.join(_to_str_list([result[6]] + result[10]))

        return result[0:3] + (aal_labels, result[4], ba_idxs, ba_labels, result[7])


cleanScreen()

while True:
    print('Input MNI coordinates seperated by anything line by line, Input *** to start querying.')
    query = []
    last_input = ''

    while last_input != '***\n':
        last_input = sys.stdin.readline()
        last_coordinate = filterInputs(last_input)

        if last_input == '***\n':
            print('[INFO] Querying, please wait...')
            continue
        
        if last_coordinate is None:
            print(
                '[WARN] The coordinates to be queried should have three dimensions, ignored.')
            continue

        if not validate_range(last_coordinate[0], last_coordinate[1], last_coordinate[2]):
            print('[WARN] The coordinate exceeds the bounding box, ignored.')
            continue

        query.append(last_coordinate)

    query_result = list(map(_query_brain, query))

    cleanScreen()
    print()
    print(tabulate(query_result, headers=query_names))
    print()
    if not args.radius[0] is None:
      print('* Query radius is %s, threshold is %s.' % (args.radius[0], args.threshold[0]))
    
    print()
    print()
    print('Press enter to continue, Press Ctrl-C to exit.')
    sys.stdin.readline()

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
    '-i', '--input', nargs='?', type=str, metavar='inupt', dest='input', default=None,
    help='Input data source, "clipboard" for data from clipboard, "interactive" for interactive mode (default), or file path for reading data from a file'
)

parser.add_argument(
    '-o', '--output', nargs='?', type=str, metavar='output', dest='output', default=None,
    help='Output destination of your data, could be "clipboard", "cli" or a file path (don\'t support glob pattern)'
)

parser.add_argument(
    '-r', '--radius', nargs='?', type=int, metavar='radius', dest='radius', default=None,
    help='the radius of fuzzy query, if provided, brainSpy will not only query the coordinate, but also voxels around the coordinate'
)

parser.add_argument(
    '-ap', '--all-peaks', dest='all_peaks', action='store_true',
    help='for spm parser only, if keep all peaks or first peak of all clusters'
)

parser.add_argument(
    '-a', '--atlas', metavar=('name', 'items'), nargs='*', action='append',
    help='atlas config, should provide the id and the item name to be shown'
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

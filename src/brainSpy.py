import os
import sys
import argparse

from os import path

__VERSION__ = '0.0.2'
__NSAF_PATH__ = path.join(path.dirname(path.realpath(__file__)), 'data')
__DEFAULT_QUERY_ITEMS__ = [['aal', 'name'], ['ba', 'label']]

argv_p = argparse.ArgumentParser(
    description='Transform MNI coordinate to AAL and BA structural names.'
)
argv_p.add_argument(
    'parser', nargs='?', type=str, default='raw', 
    help='selecting one parser for different types of text'
)

argv_p.add_argument(
    '-i', '--input', nargs='?', type=str, metavar='pattern', dest='input', default='interactive',
    help='Input data source, "clipboard" for data from clipboard, "interactive" for interactive mode (default), or file path for reading data from a file'
)

argv_p.add_argument(
    '-o', '--output', nargs='?', type=str, metavar='path', dest='output', default='terminal',
    help='Output destination of your data, could be "clipboard", "terminal" or a file path (don\'t support glob pattern)'
)

argv_p.add_argument(
    '-r', '--radius', nargs='?', type=int, metavar='int/float', dest='radius', default=None,
    help='the radius of fuzzy query, if provided, brainSpy will not only query the coordinate, but also voxels around the coordinate'
)

argv_p.add_argument(
    '-ap', '--all-peaks', dest='all_peaks', action='store_true',
    help='for spm parser only, if keep all peaks or first peak of all clusters'
)

argv_p.add_argument(
    '-a', '--atlas', metavar=('name', 'items'), nargs='*', action='append', default=__DEFAULT_QUERY_ITEMS__,
    help='atlas config, should provide the id and the item name to be shown'
)

argv_p.add_argument(
    '-l', '--language', nargs='?', type=str, metavar='str', dest='lang', default=None,
    help='for spm parser only, if keep all peaks or first peak of all clusters'
)

argv_p.add_argument(
    '-c', '--clipboard', dest='clipboard', action='store_true',
    help='read content from clipboard, transform it and send the result to clipboard at once'
)

argv_p.add_argument(
    '-d', '--debug', dest='debug', action='store_true',
    help='enable debug mode, will throw error while failed to parse the content'
)

args = argv_p.parse_args()

__READERS__ = {
    'c': 'clipboard',
    'clip': 'clipboard',
    'clipboard': 'clipboard',
    'i': 'interactive',
    'interact': 'interactive',
    'interactive': 'interactive'
}

__PARSERS__ = {
    'r': 'raw',
    'raw': 'raw',
    's': 'spm',
    'spm': 'spm'
}

__PRODUCERS__ = {
    'c': 'clipboard',
    'clip': 'clipboard',
    'clipboard': 'clipboard',
    't': 'cli',
    'term': 'cli',
    'terminal': 'cli',
    'cli': 'cli'
}

import importlib

from common import atlas_config
from common.Queryer import Queryer
from common.AtlasSet import AtlasSet
from common import format_header

# Initialize atlas and queryer
atlas_set = AtlasSet(__NSAF_PATH__, args.lang, atlas_config.format(args.atlas))
queryer = Queryer(atlas_set)

# Initialize input source and output destinition
if args.input in __READERS__:
    Reader = importlib.import_module('readers.%s' % __READERS__[args.input])
else:
    Reader = importlib.import_module('readers.%s' % 'file')

if args.output in __PRODUCERS__:
    Producer = importlib.import_module('producers.%s' % __PRODUCERS__[args.output])
else:
    Producer = importlib.import_module('producers.%s' % 'file')

reader = Reader.Reader(args)
producer = Producer.Producer()

while True:
    # Initialize content parser
    if args.parser in __PARSERS__:
        Parser = importlib.import_module('parsers.%s' % __PARSERS__[args.parser])
        parser = Parser.Parser(atlas_set)
    else:
        print('[ERROR] Parser not found!')
        sys.exit(1)
    # Start reading data from sorce:
    reader.run(parser)

    rows = parser.fetch()

    # Producer will tell us what kind of data it need:
    d_format = producer.format
    d_simp = producer.simp

    # Start querying based on d_format
    if d_format == 'c':
        q = queryer.cquery(rows, args.radius)
        header_formater = format_header.c_format_header
    elif d_format == 'r':
        q = queryer.rquery(rows, args.radius)
        header_formater = format_header.r_format_header
    else:
        print('[ERROR] Illegal producer format, checkout the source code!')
        sys.exit(1)
    
    producer.run(header_formater(q, atlas_set, parser))

    if not reader.loop:
        break


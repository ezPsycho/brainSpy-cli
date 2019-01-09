import re
import sys

from collections import OrderedDict

from . import parser

__RE__ = r'\-?\d+'

__HEADER_DICT__ = OrderedDict([
    ('x', 'X'),
    ('y', 'Y'),
    ('z', 'Z') 
])

class RawParser(parser.Parser):
    def __init__(self, queryer, options = {'radius': None, 'threshold': 0}):
        self.header_dict = __HEADER_DICT__
        self.options = options

        super(RawParser, self).__init__(queryer)

    def filter_inputs(self, x):
        c = re.findall(__RE__, x)

        if len(c) < 3:
            return None
        else:
            return list(map(lambda x: round(float(x)), c[0:3]))

    def cli_validate(self, x):
        coordinate = re.findall(__RE__, x)

        if not len(coordinate) >= 3:
            print('[WARN] The coordinates to be queried should have three dimensions, ignored.')
            return False

        return True
    
    def parse(self, x):
        coord_str = re.findall(__RE__, x)
        coord = tuple(map(lambda y: round(float(x)), x))
        result = OrderedDict(zip(
            ('x', 'y', 'z'), 
            coord_str
        ))

        result['coord'] = coord

        return result
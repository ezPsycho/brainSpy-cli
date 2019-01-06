import re
import sys
sys.path.append("..")

import modules.brainspy.brainspy as brainspy

from collections import OrderedDict

from . import parser

def _to_str_list(x):
    return list(map(str, x))

def _to_float_list(x):
    return list(map(float, x))

class RawParser(parser.Parser):
    def __init__(self, options = {'radius': None, 'threshold': 0}, batch_mode = False):
        self.options = options
        self.regex = r'\-?\d+'
        self.cli_header = ['X', 'Y', 'Z', 'AAL Label', 'Dist.', 'BA #', 'BA Label', 'Dist.']
        self.clipboard_header = brainspy.query_keys

        super(RawParser, self).__init__(batch_mode)

    def filter_inputs(self, x):
        c = re.findall(self.regex, x)

        if len(c) < 3:
            return None
        else:
            return list(map(lambda x: round(float(x)), c[0:3]))
    
    def query_brain(self, x, sep = '\n', batch = None):
        if not x is None:
            _line_result = dict(zip(
                brainspy.query_keys + ['aal_in_range', 'ba_in_range_idx', 'ba_in_range_label'],
                brainspy.query_brain(*x, self.options['radius'], self.options['threshold'])
            ))
        
            if batch is not None and self.batch_mode:
                _line_result['batch'] = batch
            
            return _line_result

    def format_result(self, x, sep = '\n'):
        x['aal.label'] = sep.join(_to_str_list([x['aal.label'], ] + x['aal_in_range']))
        x['ba.idx'] = sep.join(_to_str_list([x['ba.idx'], ] + x['ba_in_range_idx']))
        x['ba.label'] = sep.join(_to_str_list([x['ba.label'], ] + x['ba_in_range_label']))

        del x['aal_in_range']
        del x['ba_in_range_idx']
        del x['ba_in_range_label']

        return x

    def cli_validate(self, x):
        coordinate = _to_float_list(re.findall(self.regex, x))

        if not len(coordinate) >= 3:
            print('[WARN] The coordinates to be queried should have three dimensions, ignored.')
            return False
        
        if not brainspy.validate_range(coordinate[0], coordinate[1], coordinate[2]):
            print('[WARN] The coordinate exceeds the bounding box, ignored.')
            return False

        return True
    
    def parser(self, x, batch = None):
        return list(map(lambda x: self.query_brain(self.filter_inputs(x)), x, batch = batch))

    def cli_formater(self, x):
        return list(map(self.format_result, x))

    def clipboard_formater(self, x):
        return list(map(lambda z: self.format_result(z, ', '), x))
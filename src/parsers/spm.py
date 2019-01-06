import re
import sys
sys.path.append("..")

import modules.brainspy.brainspy as brainspy

from collections import OrderedDict

from . import parser

def _is_float(value):
  try:
    result = float(value)
    return result
  except ValueError:
    return None

class SpmParser(parser.Parser):
    def __init__(self, options = {'all_peaks': False}, batch_mode = False):
        self.cli_header = [
            'Cluster FWE p', 'Cluster FDR p', 'Voxels', 'Cluster Uncor P', 'Peak FWE p', 'Peak FDR p', 'Peak t', 'Peak z', 'Peak Uncor p'
        ] + ['X', 'Y', 'Z', 'AAL Label', 'Dist.', 'BA #', 'BA Label', 'Dist.']

        self.clipboard_header = [
            'cluster.fwe.p', 'cluster.fdr.p', 'n.vox', 'cluster.unc.p', 
            'peak.fwe.p', 'peak.fdr.p', 'peak.t', 'peak.z', 'peak.unc.p'
        ] + brainspy.query_keys

        self.options = options

        super(SpmParser, self).__init__(batch_mode)
    
    def cli_validate(self, x):
        return True
    
    def parser(self, x, batch = None):
        parse_result = []

        for _input_line in x:
            _input_cells = list(map(lambda x: x.strip(), _input_line.split('\t')))
            if len(_input_cells) < 11:
                continue
            
            if _is_float(_input_cells[0]) is None and not self.options['all_peaks']:
                continue
            
            _line_coord = list(map(_is_float, re.split(r'\s+', _input_cells[9])))
            _line_label = brainspy.query_brain(_line_coord[0], _line_coord[1], _line_coord[2])

            _line_result = OrderedDict(zip(self.clipboard_header, tuple(map(_is_float, _input_cells[0:9])) + _line_label))

            if batch is not None and self.batch_mode:
                _line_result['batch'] = batch
            
            parse_result.append(_line_result)
        
        return parse_result

    def cli_formater(self, x):
        return x

    def clipboard_formater(self, x):
        return x

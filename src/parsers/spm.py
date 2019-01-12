import re
from collections import OrderedDict

from . import parser

def _is_float(value):
  try:
    result = float(value)
    return result
  except ValueError:
    return None

__HEADER_DICT__ = OrderedDict([
    ('cluster.fwe.p', 'Cluster FWE p'  ),
    ('cluster.fdr.p', 'Cluster FDR p'  ),
    ('n.vox'        , 'Voxels'         ),
    ('cluster.unc.p', 'Cluster Uncor P'),
    ('peak.fwe.p'   , 'Peak FWE p'     ),
    ('peak.fdr.p'   , 'Peak FDR p'     ),
    ('peak.t'       , 'Peak t'         ), 
    ('peak.z'       , 'Peak z'         ),
    ('peak.unc.p'   , 'Peak Uncor p'   ),
    ('x'            ,  'X'             ),
    ('y'            ,  'Y'             ),
    ('z'            ,  'Z'             ) 
])

class Parser(parser.ParserBase):
    def __init__(self, atlas_set, options = {'all_peaks': False}):
        self.header_dict = __HEADER_DICT__
        self.options = options

        super(Parser, self).__init__(atlas_set)

    def validate(self, x):
        return True
    
    def parse(self, x):
        _input_cells = list(map(lambda x: x.strip(), re.split(r'\s+', x)))
        
        if len(_input_cells) < 11:
            return None
        
        if _is_float(_input_cells[0]) is None and not self.options['all_peaks']:
            return None

        _coord_str = _input_cells[9:12]
        _fmt_input_cells = list(map(_is_float, _input_cells[0:9])) + _coord_str

        _line_result = OrderedDict(zip(
            __HEADER_DICT__.keys(), _fmt_input_cells
        ))

        _coord = tuple(map(int, _coord_str))

        _line_result['coord'] = _coord
        
        return _line_result

import re
from collections import OrderedDict

__GENERAL_DICT__ = {
    'coord': 'Coordination',
    'name': 'Name',
    'dist': 'Dist',
    'Ratio': 'Ratio',
    'label': 'Label',
    'name': 'Name',
    'idx': 'Index'
}

__RE__ = r'^\!@@(\S+)\!&&(\S+)$'

def parse_dynamic_col(x):
    m = re.match(__RE__, x)
    
    if m:
        return m.group(1, 2)
    else:
        return None

def _format_single_header(x, atlas_set, parser, simp = False):
    _x = OrderedDict()

    for _key in x:
        if not simp:
            if _key in __GENERAL_DICT__:
                _x[__GENERAL_DICT__[_key]] = x[_key]
                continue
            elif _key in parser.header_dict:
                _x[parser.header_dict[_key]] = x[_key]
                continue

        _p = parse_dynamic_col(_key)
        if _p:
            atlas_name = atlas_set[_p[0]].config['META']['id' if simp else 'name']
            atlas_item = _p[1] if simp else __GENERAL_DICT__[_p[1]]
            name_sep = '.' if simp else ' '
            key_name = '%s%s%s' % (atlas_name, name_sep, atlas_item)

            _x[key_name] = x[_key]
        else:
            _x[_key] == x[_key]
    return _x

def r_format_header(x, atlas_set, parser):
    return list(map(
        lambda y: _format_single_header(y, atlas_set, parser), 
        x
    ))

c_format_header = _format_single_header
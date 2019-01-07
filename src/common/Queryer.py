from os import path
from copy import deepcopy
from collections import OrderedDict

from NSAF.Atlas import Atlas

__DEFAULT_CONFIG__ = {'aal': ['name'], 'ba': ['label']}
class Queryer():
    def __init__(self, root, lang = None, config = __DEFAULT_CONFIG__):
        self.root = root
        self.config = config

        self.lang = lang
        self.atlas_set = {}

        for _idx in config:
            self.atlas_set[_idx] = Atlas(path.join(root, _idx), lang)

    def query(self, x, radius = None, no_coord = True):
        result = []
        
        if radius:
            add_item = ['ratio']
        else:
            add_item = ['dist']

        for _row in x:
            _coord = _row['coord']

            _row_q = {}
            for _atlas in self.atlas_set:
                _q = self.atlas_set[_atlas].query(_coord)
                _atlas_result = OrderedDict()

                for _item in self.config[_atlas] + add_item:
                    _atlas_result[_item] = _q[_item]
                
                _row_q[_atlas] = _atlas_result
        
            if no_coord:
                del _row['coord']

            result.append(self._fmt_q(_row, _row_q, bool(radius)))
        
        return result


    def _fmt_q(self, paras, q_result, radius):
        paras_list = list(paras.items())
        
        if radius:
            _fmted_q_result = q_result

            blank_paras = OrderedDict()
            for _key in paras.keys():
                blank_paras[_key] = ''
        else:
            _fmted_q_result = {}
            for _atlas in q_result:
                _fmted_q_result[_atlas] = [q_result[_atlas]]

        n_idxs = {}
        item_list = {}

        for _atlas in _fmted_q_result:
            n_idxs[_atlas] = len(_fmted_q_result[_atlas])
            item_list[_atlas] = q_result[_atlas].keys()

        result = []

        for _ in range(max(n_idxs.values())):
            _fmted_row = deepcopy(blank_paras if _ != 0 else paras_list)

            for _atlas in _fmted_q_result:
                _a_q_result = _fmted_q_result[_atlas]
                _atlas_prefix = self.atlas_set[_atlas].config['META']['id']

                if _ > n_idxs[_atlas]:
                    for _key in item_list[_atlas]:
                        _fmted_row.append(('!@@%s!&&%s' % (_atlas_prefix, _key), ''))
                else:
                    _row = _fmted_q_result[_atlas][_]

                    for _key in _fmted_q_result[_atlas][_]:
                        _fmted_row.append(('!@@%s!&&%s' % (_atlas_prefix, _key), _row[_key]))
            
            result.append(OrderedDict(_fmted_row))
        
        return result
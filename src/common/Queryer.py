from copy import deepcopy
from collections import OrderedDict

__FORCE_ROUND_ITEM__ = ['dist', 'ratio']

class Queryer():
    def __init__(self, atlas_set):
        self.query = self.cquery
        self.atlas_set = atlas_set

    def cquery(self, x, radius = None, no_coord = True):
        result = {}

        if radius:
            add_item = ['dist', 'ratio']
        else:
            add_item = ['dist']
    
        header = list(x[0].keys())

        for _atlas in self.atlas_set:
            _atlas_prefix = self.atlas_set[_atlas].config['META']['id']
            header = header + list(
                map(lambda x: self._fmt_q_key(_atlas_prefix, x), self.atlas_set.config[_atlas] + add_item)
            )
        
        for _header in header:
            result[_header] = []
    
        for _row in x:
            for _key in _row:
                result[_key].append(_row[_key])
            
            for _atlas in self.atlas_set:
                _q = self.atlas_set[_atlas].query(_row['coord'], radius)
            
                for _item in __FORCE_ROUND_ITEM__:
                    for __q in _q:
                        if _item in __q:
                            __q[_item] = round(__q[_item], 3)

                for __q in _q:
                    for _item in self.atlas_set.config[_atlas] + add_item:
                        _atlas_prefix = self.atlas_set[_atlas].config['META']['id']
                        _col = self._fmt_q_key(_atlas_prefix, _item)
                        
                        result[_col].append(__q[_item] if _item in __q else '')

        if no_coord:
            del result['coord']

        return result
    
    def rquery(self, x, radius = None, no_coord = True):
        result = []
        
        if radius:
            add_item = ['dist', 'ratio']
        else:
            add_item = ['dist']

        for _row in x:
            _coord = _row['coord']

            _row_q = {}
            for _atlas in self.atlas_set:
                _q = self.atlas_set[_atlas].query(_coord, radius)
                _row_q[_atlas] = []
                
                for __q in _q:
                    _atlas_result = OrderedDict()

                    for _item in self.atlas_set.config[_atlas] + add_item:
                        if _item not in __q:
                            _atlas_result[_item] = ''
                        else:
                            _atlas_result[_item] = __q[_item]
                    
                    _row_q[_atlas].append(_atlas_result)
        
            if no_coord:
                del _row['coord']

            result.append(self._fmt_q(_row, _row_q, bool(radius)))
        
        return result

    def _fmt_q_key(self, atlas, key):
        return '!@@%s!&&%s' % (atlas, key)

    def _fmt_q(self, paras, q_result, radius):
        paras_list = list(paras.items())
        
        if radius:
            blank_paras = []
            for _key in paras.keys():
                blank_paras.append((_key, ''))

        n_idxs = {}
        item_list = {}

        for _atlas in q_result:
            n_idxs[_atlas] = len(q_result[_atlas])
            item_list[_atlas] = q_result[_atlas][0].keys()

        result = []

        for _ in range(max(n_idxs.values())):
            _fmted_row = deepcopy(blank_paras if _ != 0 else paras_list)

            for _atlas in q_result:
                _a_q_result = q_result[_atlas]
                _atlas_prefix = self.atlas_set[_atlas].config['META']['id']
    
                if _ > (n_idxs[_atlas] - 1):
                    for _key in item_list[_atlas]:
                        _fmted_row.append((self._fmt_q_key(_atlas_prefix, _key), ''))
                else:
                    _row = q_result[_atlas][_]

                    for _key in q_result[_atlas][_]:
                        _fmted_row.append((self._fmt_q_key(_atlas_prefix, _key), _row[_key]))
            
            result.append(OrderedDict(_fmted_row))
        
        return result
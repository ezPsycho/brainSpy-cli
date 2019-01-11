from os import path
from collections import OrderedDict

from NSAF.Atlas import Atlas

__DEFAULT_CONFIG__ = {'aal': ['name'], 'ba': ['label']}

class AtlasSet(OrderedDict):
    def __init__(self, root, lang = None, config = __DEFAULT_CONFIG__):
        OrderedDict.__init__(OrderedDict())

        self.root = root
        self.config = config
        self.lang = lang

        for _idx in config:
            self[_idx] = Atlas(path.join(root, _idx),  lang)

    def ck_boundary(self, coord):
        return all(map(lambda x: self[x].ck_boundary(coord), self))
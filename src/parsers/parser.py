from copy import deepcopy
from tabulate import tabulate
from collections import OrderedDict

class ParserBase():
    def __init__(self, atlas_set):
        self.cache = []
        self.atlas_set = atlas_set

        self.validator = getattr(self, 'validate')
        self.parser = getattr(self, 'parse')

    def add(self, x, batch = None):
        if self.validator(x):
            _p = self.parser(x)

            if not _p:
                return False

            parsed_result = list(_p.items())

            if batch:
                parsed_result = [('batch', batch)] + parsed_result

            parsed_result = OrderedDict(parsed_result)

            if self.atlas_set.ck_boundary(parsed_result['coord']):
                self.cache.append(parsed_result)
            else:
                print('[WARN] The coordinate exceeds the bounding box, ignored.')

    def fetch(self):
        return self.cache
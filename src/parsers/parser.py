from copy import deepcopy
from tabulate import tabulate
from collections import OrderedDict

class Parser():
    def __init__(self, atlas_set):
        self.cache = []
        self.parsed_cache = None
        self.atlas_set = atlas_set

        self.validator = getattr(self, 'validate')
        self.parser = getattr(self, 'parse')

    def add(self, x, batch = None):
        if self.validator(x):
            parsed_result = list(self.parser(x).items())

            if batch:
                parsed_result = [('batch', batch)] + parsed_result

            if self.atlas_set.ck_boundary(parsed_result['coord']):
                self.cache.append(OrderedDict(parsed_result))
            else:
                print('[WARN] The coordinate exceeds the bounding box, ignored.')

    def fetch(self):
        return self.parsed_cache
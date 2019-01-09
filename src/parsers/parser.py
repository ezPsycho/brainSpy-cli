from copy import deepcopy
from tabulate import tabulate
from collections import OrderedDict

class Parser():
    def __init__(self, queryer):
        self.cache = []
        self.parsed_cache = None
        self.queryer = queryer

        self.validator = getattr(self, 'validate')
        self.parser = getattr(self, 'parse')

    def add(self, x, batch = None):
        if self.validator(x):
            parsed_result = list(self.parser(x).items())

            if batch:
                parsed_result = [('batch', batch)] + parsed_result

            if self.queryer(parsed_result['coord'].ck_boundary):
                self.cache.append(OrderedDict(parsed_result))
            else:
                print('[WARN] The coordinate exceeds the bounding box, ignored.')

    def fetch(self):
        return self.parsed_cache
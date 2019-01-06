from copy import deepcopy
from tabulate import tabulate

class Parser():
    def __init__(self, batch_mode = False):
        self.cache = []
        self.parsed_cache = None

        self.cli_header = getattr(self, 'cli_header')
        self.clipboard_header = getattr(self, 'clipboard_header')
        self.validator = getattr(self, 'cli_validate')

        self._parser = getattr(self, 'parser')
        self._cli_f = getattr(self, 'cli_formater')
        self._clipboard_f = getattr(self, 'clipboard_formater')

        if batch_mode:
            self.cli_header = self.cli_header + ['Batch']
            self.clipboard_header = self.cli_header + ['batch']
        
        self.batch_mode = batch_mode


    def add(self, x):
        if self.validator(x):
            self.cache.append(x)

    def parse(self):
        self.parsed_cache = self._parser(self.cache)
    
    def parse_cli(self):
        parsed_cache_calues = list(map(lambda x: list(x.values()), self._cli_f(deepcopy(self.parsed_cache))))

        return tabulate(parsed_cache_calues, headers=self.cli_header)
    
    def parse_tsv(self):
        parsed_cache_calues = list(map(lambda x: list(x.values()), self._clipboard_f(deepcopy(self.parsed_cache))))
        table_body = list(map(lambda x: '\t'.join(list(map(str, x))), parsed_cache_calues))

        return '\t'.join(self.clipboard_header) + '\n' + '\n'.join(table_body)


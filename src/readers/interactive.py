from ..common import wrapped_input
from ..common import clean_screen

__TERMINATE_MARKS__ = ['***', '****']

class InteractiveReader:
    def __init__(self):
        self.loop = True
    
    def run(self, parser, args = None):
        print("""
_ __                   __,            
( /  )         o       (               
/--< _   __, ,  _ _    `.   ,_   __  ,
/___// (_(_/(_(_/ / /_(___)_/|_)_/ (_/_
                            /|      /  
Interactive shell          (/      '   

==========================================
        """)

        last_input = ''

        while last_input not in __TERMINATE_MARKS__:
            last_input = wrapped_input()

            if last_input in __TERMINATE_MARKS__:
                print('[INFO] Querying, please wait...')
                return last_input

            parser.add(last_input)


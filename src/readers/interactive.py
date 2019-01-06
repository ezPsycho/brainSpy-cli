from ..common import wrapped_input
from ..common import clean_screen

terminate_marks = ['***', '****']

def interactiveReader(x, parser, src = None):
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

    while last_input not in _terminate_marks:
        last_input = wrapped_input()

        if last_input in terminate_marks:
            print('[INFO] Querying, please wait...')
            return last_input

        parser.add(last_input)


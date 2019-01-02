def cliProducer(parser, dest = None):
    with open(file, 'w') as f:
        if not f.writable:
            print('[ERROR] File is not writable.')
            return False
        
        f.write(parser.parse_tsv())

        return True
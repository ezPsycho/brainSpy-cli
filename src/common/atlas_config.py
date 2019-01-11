def format(x):
    result = {}

    for _config in x:
        if len(_config) < 2:
            continue
        
        result[_config[0]] = _config[1:]
    
    return result
def parse_args(r_args):
    args = {key:value for (key,value) in r_args.items() if key != 'api_key'}
    return args
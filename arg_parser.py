import argparse


def parse(prog: str):
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument('files', action='extend', nargs='*', type=str)
    args = parser.parse_args()
    if len(args.files) == 0: raise TypeError("Must include one or more file paths.")
    return args



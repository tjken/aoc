import argparse
import sys
from typing import Iterable, Callable


def aoc_main(prog_name: str, functions: Iterable[Callable]):
    args = parse(prog_name)

    results = []
    for file in args.files:
        with open(file) as f:
            _input = f.readlines()

        func_results = []
        for f in functions: func_results.append(f(_input))

        results.append((file, func_results))

    for r in results:
        result_strings = [f"--{r[0]}--\n"]
        for idx, val in enumerate(r[1]):
            result_strings.append(f"P{idx + 1}: {val}\n")

        print("".join(result_strings))

    sys.exit()


def parse(prog: str):
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument('files', action='extend', nargs='*', type=str)
    args = parser.parse_args()
    if len(args.files) == 0: raise TypeError("Must include one or more file paths.")
    return args

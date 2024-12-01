import arg_parser

word_nums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def get_num_1(s: str):
    r = "".join(n for n in s if n.isdigit())
    if len(r) == 0: return 0 # This is a hack to stop errors in one of the test files; part 1 doesn't define this case.
    return int(r[0] + r[-1])

def get_num_2(s: str):
    for i, num in enumerate(word_nums):
        s_idx = 0
        while s[s_idx:].count(num):
            s_idx += s[s_idx:].index(num)
            b = bytearray()
            b.extend(map(ord, s))
            b.insert(s_idx + 1, ord(str(i + 1)))
            s = b.decode()

    return get_num_1(s)


def main(files: list[str]) -> None:
    """Performs logic for the 2023 Advent of Code Day 1 puzzle, ---Trebuchet?!---

    This file takes one or more files formatted for this puzzle and provides correct output as per the requirements for
    parts 1 and 2. For more information on this puzzle, please refer to https://adventofcode.com/2023/day/1

    :param files: filepaths to be parsed
    :return:
    """
    results = []
    for file in files:
        with open(file) as f:
            _input = f.readlines()

        p1 = sum(map(get_num_1, _input))
        p2 = sum(map(get_num_2, _input))

        results.append((file, p1, p2))

    for r in results:
        print(f'--{r[0]}--\nP1: {r[1]}\nP2: {r[2]}')
    return


if __name__ == '__main__':
    import sys

    args = arg_parser.parse('01.py')
    sys.exit(main(args.files))

#!/usr/bin/env python3
from typing import Iterable

from lib import aoc_main

word_nums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def part_1(input_: Iterable[str]):
    sum_ = 0
    for line in input_:
        r = "".join(n for n in line if n.isdigit())

        # This is a hack to stop errors in one of the test files; part 1 doesn't define this case.
        if len(r) == 0: return 0

        sum_ += int(r[0] + r[-1])

    return sum_


def part_2(input_: Iterable[str]):
    processed_lines = []
    for line in input_:
        for i, num in enumerate(word_nums):
            s_idx = 0
            while line[s_idx:].count(num):
                s_idx += line[s_idx:].index(num)
                b = bytearray()
                b.extend(map(ord, line))
                b.insert(s_idx + 1, ord(str(i + 1)))
                line = b.decode()
        processed_lines.append(line)

    return part_1(processed_lines)


if __name__ == '__main__':
    aoc_main('01.py', [part_1, part_2])

#!/usr/bin/env python3
"""Advent of Code 2024 - Day 1: Historian Hysteria

This script is written to complete a puzzle from the Advent of Code 2024 event. For puzzle information,
please visit https://adventofcode.com/2024/day/1

All the scripts in this repository use a shared lib module to facilitate their standalone executable
functions.
"""

from typing import Iterable

from lib import aoc_main


def part_1(input_: Iterable[str]):
    lists = _build_lists(input_)
    # lists comes unsorted, part 1 needs them sorted
    for i in lists: i.sort()

    sum_ = 0
    # I'm assuming the lists are both the same length
    for i in range(len(lists[0])):
        # Input does not guarantee the sorted list pairs will all be (lesser, greater)
        sum_ += abs(lists[1][i] - lists[0][i])

    return sum_


def part_2(input_: Iterable[str]):
    pass


def _build_lists(input_: Iterable[str]):
    lists = ([], []) # The puzzle input is only two columns
    for line in input_:
        i = line.strip().split()
        for idx, val in enumerate(i):
            lists[idx].append(int(val))

    # Part 1 specifies that these lists will be sorted, but I'm leaving it out until Part 2
    return lists


if __name__ == '__main__':
    aoc_main('01.py', [part_1, part_2])  # TODO Add file name

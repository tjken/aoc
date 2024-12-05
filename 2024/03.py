#!/usr/bin/env python3
"""Advent of Code 2024 - Day 3: Mull It Over

This script is written to complete a puzzle from the Advent of Code 2024 event. For puzzle information,
please visit https://adventofcode.com/2024/day/3

All the scripts in this repository use a shared lib module to facilitate their standalone executable
functions.
"""
import math
import re
from typing import Iterable

from lib import aoc_main

command_mul = re.compile("mul\(\d+,\d+\)")
command_do = re.compile("do\(\)")
command_dont = re.compile("don't\(\)")


def part_1(input_: Iterable[str]) -> int:
    input_ = _add_new_lines(input_)
    items = map(_get_nums, command_mul.findall(input_))

    sum_ = 0
    for item in items:
        sum_ += math.prod(item)

    return sum_


def part_2(input_: Iterable[str]):
    DO = 1
    DONT = 2
    input_ = _add_new_lines(input_)
    items = re.compile("do\(\)|don't\(\)|mul\(\d+,\d+\)").findall(input_)

    do_flag = DO
    sum_ = 0
    for item in items:
        if do_flag == DO and item[0] == 'm':
            sum_ += math.prod(_get_nums(item))
            continue

        if do_flag == DO and item == "don't()":
            do_flag = DONT
            continue

        if do_flag == DONT and item == "do()":
            do_flag = DO
            continue

    return sum_


def _add_new_lines(lines: Iterable[str]) -> str:
    """Add new-line escape sequences to a list of strings.

    In this puzzle, the input provided is not intentionally encoded as data items separated by new-lines, so
    any \n need to be preserved. However, the aoc_main function automatically removes these and splits file
    input line by line, so this function exists to fix the input.
    """
    return "\n".join(lines)


def _get_nums(s: str) -> tuple[int, int]:
    i1, i2 = s.removeprefix('mul(').removesuffix(')').split(',')
    return int(i1), int(i2)


if __name__ == '__main__':
    aoc_main('03.py', [part_1, part_2])

#!/usr/bin/env python3
"""Advent of Code 2024 - Day 2: Red-Nosed Reports

This script is written to complete a puzzle from the Advent of Code 2024 event. For puzzle information,
please visit https://adventofcode.com/2024/day/2

All the scripts in this repository use a shared lib module to facilitate their standalone executable
functions.
"""
from enum import Enum
from typing import Iterable

from lib import aoc_main, logging

logger = logging.get_debug_logger()

def part_1(input_: Iterable[str]) -> int:
    reports = _build_reports(input_)
    return len(_validate_reports(reports)[0])


def part_2(input_: Iterable[str]):
    reports = _build_reports(input_)
    valid, invalid = _validate_reports(reports)

    l_invalid = []
    # Try and dampen invalid reports
    for r in invalid:
        dampen_reports = _dampen(r[0], r[1])
        d_valid, d_invalid = _validate_reports(dampen_reports)
        if len(d_valid) > 0:
            valid.append(d_valid[0])
        else:
            l_invalid.append(d_invalid)

    #logger.debug(msg=l_invalid)
    return len(valid)



def _build_reports(input_: Iterable[str]) -> list[list]:
    reports = []
    for line in input_:
        reports.append(list(map(int, line.strip().split())))

    return reports

def _dampen(report: list[int], error_idx, brute=True) -> list[list[int]]:
    new_reports = []

    if brute:
        for i in range(len(report)):
            report_copy = report[:]
            report_copy.pop(i)
            new_reports.append(report_copy)

    # Ongoing attempt at solving without brute force. It almost works.
    else:
        # There's an edge case if error reports an index of 1 or 2; need to check index 0 as well
        if error_idx == 1 or error_idx == 2:
            new_reports.append(report[1:])

        report_copy = report[:]
        report_copy.pop(error_idx)
        new_reports.append(report_copy)

    return new_reports


def _is_safe(report: Iterable[int]) -> None:
    # Iterator loop needs to know the direction it's trending, and the previous number
    direction = None
    prev_num = None
    for idx, num in enumerate(iter(report)):
        # Sets first prev_num; loops
        if prev_num is None:
            prev_num = num
            continue

        difference = num - prev_num
        # Changes that aren't between the values of 1 to 3 are considered unsafe
        if abs(difference) not in range(1, 4): raise ValueError("Report is unsafe", idx)

        # Sets direction on second number; set new prev_num before looping
        if direction is None:
            direction = _Direction.ASCENDING if difference > 0 else _Direction.DESCENDING
            prev_num = num
            continue

        # If difference isn't consistent, it's considered unsafe
        if (direction is _Direction.ASCENDING and difference < 0) or \
                (direction is _Direction.DESCENDING and difference > 0):
            raise ValueError("Report is unsafe", idx)

        # Set new prev_num before continuing loop
        prev_num = num

    # Exit _is_safe


def _validate_reports(reports: Iterable) -> tuple[list, list]:
    validated_reports = []
    invalidated_reports = []

    for r in reports:
        try:
            _is_safe(r)
            validated_reports.append(r)
        except ValueError as err:
            invalidated_reports.append((r, err.args[1]))

    return validated_reports, invalidated_reports


class _Direction(Enum):
    ASCENDING = 1
    DESCENDING = 2


if __name__ == '__main__':
    aoc_main('02.py', [part_1, part_2])

#!/usr/bin/env python3
"""Advent of Code 2024 - Day 4: Ceres Search

This script is written to complete a puzzle from the Advent of Code 2024 event. For puzzle information,
please visit https://adventofcode.com/2024/day/4

All the scripts in this repository use a shared lib module to facilitate their standalone executable
functions.
"""
from copy import deepcopy
from itertools import product
from operator import add
from typing import Iterable

from lib import aoc_main


def part_1(input_: Iterable[str]):
    board = _Board(list(input_))
    word = "XMAS"

    return _find_word_sum(word, board)


def part_2(input_: Iterable[str]):
    pass


class _Board:
    """Class representing the crossword board.

    This puzzle seems similar to boggle, which I have previously coded something like before."""

    def __init__(self, board_str_list: list[str]):
        self._board = deepcopy(board_str_list)
        self.x_bounds = len(self._board)
        self.y_bounds = len(self._board[0])

    def get_idx(self, idx: tuple[int, int]) -> str | None:
        if idx[0] < 0 or idx[1] < 0:
            return None
        try:
            return self._board[idx[0]][idx[1]]
        except IndexError:
            return None


def _find_word_sum(word: str, board: _Board) -> int:
    """Find the total number of times a word appears in a _Board instance

        :param word: string to search for
        :param board: _Board instance to check
        :return: int sum of time the given word appears
    """
    # Use a prefix table to short-circuit out of bad word reads.
    prefixes = set()
    for index in range(1, len(word)): prefixes.add(word[:index])

    # Relative indices to search for words in; words must be in one direction
    directions = (
        tuple(filter(lambda x: x != (0, 0), product(range(-1, 2), repeat=2))))
    indices = product(range(board.x_bounds), range(board.y_bounds))
    sum_ = 0

    # For each board index, in each direction
    lookups = product(indices, directions)
    for index, direction in lookups:
        working_str = board.get_idx(index)
        # Short circuit if the first letter is wrong
        if working_str not in prefixes: continue

        while 0 < len(working_str) < len(word):
            # If working_str is not correct, break loop and fail later comparison
            if working_str not in prefixes: break

            # Otherwise, get the next letter and try again
            index = tuple(map(add, index, direction))
            try:
                working_str += board.get_idx(index)
            except TypeError:
                break

            # Check if working_str, is now none, and force a failed comparison if so
            if working_str is None:
                working_str = ""
                break

        if working_str == word: sum_ += 1

    return sum_


if __name__ == '__main__':
    aoc_main('04.py', [part_1, part_2])  # TODO Add file name

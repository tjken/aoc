#!/usr/bin/env python3
"""Advent of Code 2024 - Day 4: Ceres Search

This script is written to complete a puzzle from the Advent of Code 2024 event. For puzzle information,
please visit https://adventofcode.com/2024/day/4

All the scripts in this repository use a shared lib module to facilitate their standalone executable
functions.
"""
from copy import deepcopy
from itertools import product
from typing import Iterable

from lib import aoc_main


def part_1(input_: Iterable[str]):
    board = _Board(input_)
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
        try:
            return self._board[idx[0]][idx[1]]
        except IndexError:
            return None

def _find_word_sum(word: str, board: _Board) -> int:
    # Use a prefix table to short-circuit out of bad word reads.
    prefixes = set()
    for idx in range(1, len(word)+1): prefixes.add(word[:idx])

    # Relative indices to search for words in; words must be in one direction
    direction_idxs = (
        tuple(filter(lambda x: x != (0, 0), product(range(-1, 2), repeat=2))))
    board_idxs = product(range(board.x_bounds), range(board.y_bounds))
    sum_ = 0
    # For each index, in each relative direction
    for idx in board_idxs:
        working_str = board.get_idx(idx)
        # If the first letter isn't the start of the word, continue
        if working_str not in prefixes: continue

        for dir_ in direction_idxs:
            # If a direction is a match, partial or full, working_str needs to be reset
            if len(working_str) > 1: working_str = board.get_idx(idx)

            working_idx = deepcopy(idx)
            while len(working_str) < len(word):
                new_idx = working_idx[0] + dir_[0], working_idx[1] + dir_[1]
                inspected_char = board.get_idx(new_idx) or "~"

                # If index doesn't exist, or the prefix is wrong, break inner loop.
                if working_str + inspected_char not in prefixes:
                    break
                else:
                    working_str = working_str + inspected_char
                    working_idx = new_idx
                # End inner loop

            if working_str == word: sum_ += 1

            # End dir_
        # End idx loop

    return sum_





if __name__ == '__main__':
    aoc_main('04.py', [part_1, part_2])  # TODO Add file name

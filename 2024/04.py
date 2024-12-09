#!/usr/bin/env python3
"""Advent of Code 2024 - Day 4: Ceres Search

This script is written to complete a puzzle from the Advent of Code 2024 event. For puzzle information,
please visit https://adventofcode.com/2024/day/4

All the scripts in this repository use a shared lib module to facilitate their standalone executable
functions.
"""
import operator
from copy import deepcopy
from itertools import product
from operator import add
from typing import Iterable

from lib import aoc_main

# Relative indices to search for words in; words must be in one direction
DIRECTIONS = (tuple(filter(lambda x: x != (0, 0), product(range(-1, 2), repeat=2))))
# Filter DIRECTIONS to only include diagonals (needed for part 2)
X_DIRECTIONS = (
    tuple(
        filter(lambda x: x[0] != 0 and x[1] != 0, DIRECTIONS)
    )
)


def part_1(input_: Iterable[str]):
    board = _Board(list(input_))
    word = "XMAS"

    return len(_find_word(word, board))


def part_2(input_: Iterable[str]):
    raise NotImplementedError
    board = _Board(list(input_))
    word = "MAS"

    return _find_intersections(word, board)


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


def _map_lookups(locations, distance: int):
    x_location_complement_mult = (1, -1)
    y_location_complement_mult = (-1, 1)

    lookups = []

    for index, direction in locations:
        # Get complementary directions for the given direction
        x_relative_direction = (
            tuple(map(operator.mul, direction, x_location_complement_mult))
        )
        y_relative_direction = (
            tuple(map(operator.mul, direction, y_location_complement_mult))
        )

        # Get relative indices to check; these values will be added to the
        # current index value.
        x_relative_index_mod = 0, distance * direction[0]
        y_relative_index_mod = distance * direction[1], 0

        x_relative_index = tuple(map(operator.add, index, x_relative_index_mod))
        y_relative_index = tuple(map(operator.add, index, y_relative_index_mod))

        lookups.append(
            tuple([
                (index, direction),
                tuple([
                    (x_relative_index, x_relative_direction),
                    (y_relative_index, y_relative_direction)
                ])
            ])
        )

    return lookups


def _find_intersections(word: str, board: _Board):
    """Find x-shaped intersections of a given word in a given board.

    :param word: word being searched for
    :param board: _Board instance to check
    :return: TODO
    """
    locations = _find_word(word, board)
    # Filter locations to only include words found along diagonals
    locations = tuple(filter(lambda x: x[1] in X_DIRECTIONS, locations))

    lookups = _map_lookups(locations, len(word) - 1)
    sum_ = 0
    for location, new_locations in lookups:
        for compare_ in new_locations:
            if compare_ in locations: sum_ +=1


    return int(sum_ / 2)


def _find_word(word: str, board: _Board) -> list[tuple]:
    """Find the total number of times a word appears in a _Board instance

        :param word: string to search for
        :param board: _Board instance to check
        :return: list of indices and directions where the given word is found
    """
    # Use a prefix table to short-circuit out of bad word reads.
    prefixes = set()
    for index in range(1, len(word)): prefixes.add(word[:index])

    indices = product(range(board.x_bounds), range(board.y_bounds))
    matches = []

    # For each board index, in each direction
    lookups = product(indices, DIRECTIONS)
    for index, direction in lookups:
        current_lookup = deepcopy(index), direction
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

        if working_str == word: matches.append(current_lookup)

    return matches


if __name__ == '__main__':
    aoc_main('04.py', [part_1, part_2])  # TODO Add file name

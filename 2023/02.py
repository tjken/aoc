#!/usr/bin/env python3
from math import prod
from typing import Iterable

from lib import aoc_main

comparison = {'red': 12, 'green': 13, 'blue': 14}


def read_games(inputs_: iter) -> dict:
    values = dict()
    for game in inputs_:
        c_idx = game.index(':')
        game_id = _read_num_from_str(game[:c_idx])
        game_results = _read_results_from_str(game[c_idx:])

        values[game_id] = game_results

    return values


def _read_num_from_str(s: str) -> int:
    result = ''.join(filter(lambda x: x.isdigit(), s))
    return int(result)


def _read_results_from_str(s: str) -> dict:
    results = dict()
    # strip leading colon
    games = s.strip(':').split(';')
    # check each split
    for game in games:
        items = game.split(',')
        for item in items:
            x, y = item.strip().split(' ')
            if y not in results:
                results[y] = int(x)
            elif int(x) > results[y]:
                results[y] = int(x)

    return results


def _lt_dict(d1, d2) -> bool:
    for key in d1.keys():
        if d1[key] > d2[key]: return False

    return True


def part_1(inputs_: Iterable[str]) -> int:
    games = read_games(inputs_)
    s = 0
    for key in games.keys():
        if _lt_dict(games[key], comparison): s += key

    return s


def part_2(inputs_: Iterable[str]) -> int:
    games = read_games(inputs_)
    s = 0
    for entry in games.values():
        s += prod(list(entry.values()))

    return s


if __name__ == '__main__':
    aoc_main('02.py', [part_1, part_2])

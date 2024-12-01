import math
from typing import Iterable

from lib import aoc_main


class Game:
    id_: int
    numbers: set[int]
    winning_numbers: set[int]

    def __init__(self, info: str):
        # Reformat the info string; now formatted in a list as:
        # {game_id}: winning numbers | numbers
        info_ = info.removeprefix("Card").strip().split()

        self.id_ = int(info_.pop(0).removesuffix(':'))
        separator_idx = info_.index('|')
        self.winning_numbers = set(map(int, info_[:separator_idx]))
        self.numbers = set(map(int, info_[separator_idx + 1:]))

    def matching_numbers(self) -> set[int]:
        return set.intersection(self.numbers, self.winning_numbers)


def main(files: list[str, ...]):
    results = []
    for file in files:
        with open(file) as f:
            input_ = f.readlines()

        p1 = part_1(input_)
        p2 = part_2(input_)

        results.append((file, p1, p2))

    for r in results:
        print(f'--{r[0]}--\nP1: {r[1]}\nP2: {r[2]}')
    return


def part_1(games: Iterable[str]):
    sum_ = 0
    for game in games:
        game = Game(game)
        nums = len(game.matching_numbers())
        if nums == 0:
            continue
        sum_ += int(math.exp2(nums - 1))

    return sum_


def part_2(games: Iterable[str]):
    sum_ = 0
    additional_cards_queue = [0]
    for game in games:
        game = Game(game)
        cards = 1 + additional_cards_queue.pop(0)
        sum_ += cards

        # Handle additional cards
        additional_cards = len(game.matching_numbers())
        if additional_cards:
            # Check if the queue has enough spots for additional cards; make 0s if not
            difference = additional_cards - len(additional_cards_queue)
            if difference > 0:
                for _ in range(difference): additional_cards_queue.append(0)

            for i in range(additional_cards):
                additional_cards_queue[i] += cards

        # If additional_cards_queue happens to be empty, fill it with a 0 value
        elif len(additional_cards_queue) == 0:
            additional_cards_queue.append(0)

    return sum_


if __name__ == '__main__':
    aoc_main("04.py", [part_1, part_2])

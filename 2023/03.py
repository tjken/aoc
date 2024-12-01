#!/usr/bin/env python3
import sys
from lib import aoc_main
from itertools import product
from math import prod
from typing import TypeAlias

Item: TypeAlias = tuple[int, str]  # ID number, Value string (ie '234', or '#')

# Tuple to use when finding relative indexes ((-1, -1), (-1, 0), (-1, 1), ... (1, 1))
_comparison_idx_range = tuple(filter(lambda x: x != (0, 0), product(range(-1, 2), repeat=2)))


def _build_item_table(lines) -> dict:
    def add_number(x_idx, num_info_) -> None:
        """Add a number to item_table at a given index.

        Numbers are taken and stored as a string. Since numbers are non-unique, they are assigned an id number,
        and it's used as its key in the table. If a number is more than a single digit in length, the whole
        number is read and assigned to every index it's found in.

        The parameters for this function are holdovers from an old helper function. It's not great, but a
        possible rewrite is not in consideration at the moment.

        :param x_idx: x-index of the numbers location in the table.
        :param num_info_: information used by the _build_item_table function to help make a number entry.
        :return: None
        """

        """The num_info_ format goes as follows:
            1: a bool flag indicating working number information; this function resets this to False before
            returning.

            2: the y-index of the working number; if the number is more than one digit long, this function will
            assign it to all y-indices it occupies.

            3: the working number value, as a string.
        """
        num = num_info_[2]
        index = x_idx, num_info_[1]
        _id = _generate_item_id()
        # Adds the number to every index it occupies into the item_table
        for i in range(len(num)): item_table[(index[0], index[1] + i)] = (_id, num)

        num_info_[0] = False

    def add_machine_part(s: str, idx: tuple[int, int]) -> None:
        """Adds a machine part to item_table.

        :param s: string representing the part. It should only be one character.
        :param idx: tuple represeting the x, y coordinates of the part in the table.
        :return: None
        """
        _id = _generate_item_id()
        item_table[idx] = (_id, s)

    item_table = dict()  # Use coordinates as a tuple (x, y) for keys; use Items for values.
    # If a number is multiple digits, need to know and keep track of current info
    num_info: list[bool | int | str] = [False, -1, '']
    # search lines for numbers and machine symbols
    for idx_x, line in enumerate(lines):  # TODO: Check if we can use product for x,y coordinates
        # If there is num_info when checking a new line, then the previous line ended with a number.
        if num_info[0]: add_number(idx_x - 1, num_info)

        for idx_y, ch in enumerate(line):
            if _is_number(ch):
                # Start storing number data; will get finalized on a later enumeration
                if num_info[0] is False:
                    num_info = [True, idx_y, ''.join(ch)]
                else:
                    num_info[2] += ch

                continue

            # Add previous number data if it's stored before checking other possibilities
            if num_info[0]: add_number(idx_x, num_info)

            if _is_machine_part(ch):
                # Register machine part if found
                add_machine_part(ch, (idx_x, idx_y))
                continue

            # End of inner loop
        # End of outer loop
    # If there's number info still in num_info, add it to the table.
    if num_info[0]:
        add_number(len(lines) - 1, num_info)
    return item_table


def _generate_item_id() -> int:
    _id = 0
    while _id < sys.maxsize:
        yield _id
        _id += 1


def _get_relative_idxs(index: tuple[int, int]) -> list[tuple[int, int]]:
    l = []
    for idx in _comparison_idx_range:
        l.append((index[0] + idx[0], index[1] + idx[1]))
    return l


def _is_machine_part(ch: str) -> bool:
    if ch.isdigit() or ch == '.' or ch == '\n':
        return False
    else:
        return True


def _is_number(s: str) -> bool:
    return s.isdigit()


def _part_0(lines: list) -> list[tuple[Item, dict]]:
    """Perform shared logic between part_1 and part_2

    part_2 requires knowing which numbers connect to which gears. While part_1 only needs connected numbers, this
    function will return an iter of all gears, plus their connected numbers. It is up to calling functions (part_1 and
    part_2) to use what they need.
    """

    items = _build_item_table(lines)
    gears: list[tuple[Item, dict]] = []
    # Find machine parts and collect their adjacent numbers
    for idx in items.keys():
        # Pass over any non-machine part index
        if not _is_machine_part(items[idx][1]): continue

        gear = items[idx]
        nums = {}

        # Search for numbers surrounding the current index
        for i in _get_relative_idxs(idx):
            item = items.get(i)
            if item is None: continue

            # Add any numbers to the value_items set
            if _is_number(item[1]): nums[item[0]] = int(item[1])

        gears.append((gear, nums))

    return gears


def part_1(lines: list) -> int:
    value_items = {}
    gears = _part_0(lines)

    for gear in gears: value_items.update(gear[1])
    return sum(value_items.values())


def part_2(lines: list) -> int:
    _sum = 0
    gears = _part_0(lines)

    for gear in gears:
        if len(gear[1]) < 2: continue
        nums = []
        for num in gear[1].values(): nums.append(num)
        _sum += prod(nums)
    return _sum


if __name__ == "__main__":
    aoc_main('03.py', [part_1, part_2])

import sys
import arg_parser
from itertools import product
from math import prod
from typing import TypeAlias

Item: TypeAlias = tuple[int, str]  # ID number, Value string (ie '234', or '#')

# Tuple to use when finding relative indexes ((-1, -1), (-1, 0), (-1, 1), ... (1, 1))
_comparison_idx_range = tuple(filter(lambda x: x != (0, 0), product(range(-1, 2), repeat=2)))


def _build_item_table(lines) -> dict:
    def add_number(num: str, idx: tuple[int, int]):
        _id = _generate_item_id()
        for i in range(len(num)): item_table[(idx[0], idx[1] + i)] = (_id, num)

    def _add_num_info(x_idx, num_info_): # TODO: Fold this function into add_number
        add_number(num_info_[2], (x_idx, num_info_[1]))
        num_info_[0] = False

    def add_machine_part(s: str, idx: tuple[int, int]):
        _id = _generate_item_id()
        item_table[idx] = (_id, s)

    item_table = dict()  # Use coordinates as a tuple (x, y) for keys; use Items for values.
    # If a number is multiple digits, need to know and keep track of current info
    num_info: list[bool | int | str] = [False, -1, '']
    # search lines for numbers and machine symbols
    for idx_x, line in enumerate(lines):  # TODO: Check if we can use product for x,y coordinates
        # If there is num_info when checking a new line, then the previous line ended with a number.
        if num_info[0]: _add_num_info(idx_x - 1, num_info)

        for idx_y, ch in enumerate(line):
            if _is_number(ch):
                # Start storing number data; will get finalized on a later enumeration
                if num_info[0] is False:
                    num_info = [True, idx_y, ''.join(ch)]
                else:
                    num_info[2] += ch

                continue

            # Add previous number data if it's stored before checking other possibilities
            if num_info[0]: _add_num_info(idx_x, num_info)

            if _is_machine_part(ch):
                # Register machine part if found
                add_machine_part(ch, (idx_x, idx_y))
                continue

            # End of inner loop
        # End of outer loop
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
    if ch.isdigit() or ch == '.':
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


def main(files: list[str, ...]) -> None:
    results = []
    for file in files:
        with open(file) as f:
            _input = f.readlines()

        p1 = part_1(_input)
        p2 = part_2(_input)

        results.append((file, p1, p2))

    for r in results:
        print(f'--{r[0]}--\nP1: {r[1]}\nP2: {r[2]}')
    return

if __name__ == "__main__":
    args = arg_parser.parse("03.py")

    sys.exit(main(args.files))


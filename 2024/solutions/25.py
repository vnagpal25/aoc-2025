import os
import pdb
from tqdm import tqdm
from collections import deque
from functools import cache
from itertools import product
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""
pt1_ans: int = 3
pt2_ans: int = 0


def parse_input(string: str):
    locks = []
    keys = []
    for block in string.split('\n\n'):
        block = block.splitlines()
        if block[0] == '#' * len(block[0]):
            locks.append(block)
        else:
            keys.append(block)

    return locks, keys


def pt1(locks, keys):
    height = len(locks[0]) - 1

    # tranpose each lock using zip(*lock) to iterate over columns
    # strip the 1st character and tailing '.' to count number of # in the column
    # do the reverse for keys
    locks = [[len(''.join(column[1:]).strip('.'))
              for column in zip(*lock)] for lock in locks]

    keys = [[len(''.join(column[::-1][1:]).strip('.'))
             for column in zip(*key)] for key in keys]

    # traverse over each combination of lock and keys
    count = 0
    for lock, key in product(locks, keys):
        # go through each pair of key and lock heights and if one pair violates the overlapping condition, we break and don't increment,
        # else we increment the counter
        for li, ki in zip(lock, key):
            if li + ki >= height:
                break
        else:
            count += 1
    return count


def pt2():
    return pt2_ans


def main(puzzle: str):
    assert pt1_ans == pt1(*parse_input(test))
    print(f"Part 1: {pt1(*parse_input(puzzle))}")

    # assert pt2_ans == pt2(test)
    # print(f"Part 2: {pt2(puzzle)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

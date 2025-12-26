import os
import pdb
from tqdm import tqdm
from collections import deque
from functools import cache
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

# TODO replace with test input and corresponding answers
test: str = """
"""
pt1_ans: int = 0
pt2_ans: int = 0


def parse_input(string: str):
    ...


def pt1():
    return pt1_ans


def pt2():
    return pt2_ans


def main(puzzle: str):
    # TODO parse input and test

    assert pt1_ans == pt1(test)
    print(f"Part 1: {pt1(puzzle)}")

    assert pt2_ans == pt2(test)
    print(f"Part 2: {pt2(puzzle)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

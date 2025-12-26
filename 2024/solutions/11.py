import os
from typing import *
from functools import cache
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """125 17"""
pt1_ans: int = 55312
pt2_ans: int = 0


def parse_input(string: str):
    return string.strip().split()


def pt1(arr: List[str]) -> int:
    """
    Rules:
    - 0 is replaced with 1
    - Even digits are split in two stones with left digits and right digits.(drop leading zeros)
    If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
    """

    # naive solution, doing computation for each element in array and storing a new array
    for _ in range(25):
        new_arr = []

        for el in arr:
            if el == '0':
                new_arr.append('1')
            elif len(el) % 2 == 0:
                l: str = el[:len(el) // 2]
                r: str = el[len(el) // 2:]
                new_arr.append(l)
                while r.startswith('0') and len(r) > 1:
                    r = r[1:]
                new_arr.append(r)
            else:
                new_arr.append(str(int(el) * 2024))
        arr = new_arr
    return len(arr)


def pt2(stones: List[str]) -> int:
    """
    Rules:
    - 0 is replaced with 1
    - Even digits are split in two stones with left digits and right digits.(drop leading zeros)
    If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
    """

    # cached solution, the idea here is that we know that the relative order of stones in the array never changes
    # so we count how many stones one stone becomes after n steps in a recursive manner and cache it to avoid repeated computation
    @cache
    def count(stone, steps):
        # base case, no more steps to go
        if steps == 0:
            return 1
        # convert stone to a 1
        if stone == 0:
            return count(1, steps - 1)
        string = str(stone)
        length = len(string)
        # count left and right portions of string
        if length % 2 == 0:
            return count(int(string[:length//2]), steps-1) + count(int(string[length//2:]), steps-1)
        # multiply by 2024
        else:
            return count(stone * 2024, steps - 1)

    stones = [int(x) for x in stones]

    ret = sum(count(x, 75) for x in stones)

    stats = count.cache_info()
    print(f"Cache hits: {stats.hits}, Cache misses: {stats.misses}")

    return ret


def main(puzzle: str):
    test_arr = parse_input(test)
    arr = parse_input(puzzle)
    print(test_arr)
    assert pt1_ans == pt1(test_arr)
    print(f"Part 1: {pt1(arr)}")

    print(f"Part 2: {pt2(arr)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

import os
import pdb
from tqdm import tqdm
from collections import deque
from functools import cache
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test1: str = """1
10
100
2024
"""
pt1_ans: int = 37327623

test2: str = """1
2
3
2024
"""
pt2_ans: int = 23


def parse_input(string: str):
    return list(map(int, string.strip().splitlines()))


def pt1(nums):
    def secret_number(num, times):
        for _ in range(times):
            num = (num ^ (num * 64)) % 16777216
            num = (num ^ (num // 32)) % 16777216
            num = (num ^ (num * 2048)) % 16777216
        return num
    total = 0
    for num in nums:
        total += secret_number(num, 2000)

    return total


def pt2(nums):
    def secret_number(num):
        num = (num ^ (num * 64)) % 16777216
        num = (num ^ (num // 32)) % 16777216
        num = (num ^ (num * 2048)) % 16777216
        return num

    sequence_banana_map = {}

    for num in nums:
        buyer = [num % 10]
        for _ in range(2000):
            num = secret_number(num)
            buyer.append(num % 10)
        seen = set()

        # we are analyzing 4 differences in prices, so we need all adjacent 5-tuples
        for i in range(len(buyer) - 4):
            five_tuple = buyer[i:i+5]
            differences = tuple(
                [y - x for x, y in zip(five_tuple, five_tuple[1:])])
            if differences in seen:
                continue
            seen.add(differences)

            if differences not in sequence_banana_map:
                sequence_banana_map[differences] = 0

            sequence_banana_map[differences] += five_tuple[-1]

    return max(sequence_banana_map.values())


def main(puzzle: str):
    test_nums = parse_input(test1)
    nums = parse_input(puzzle)

    assert pt1_ans == pt1(test_nums)
    print(f"Part 1: {pt1(nums)}")

    test_nums = parse_input(test2)
    assert pt2_ans == pt2(test_nums)
    print(f"Part 2: {pt2(nums)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

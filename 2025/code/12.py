import os
import re

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    trees = puzzle.split("\n\n")[-1].splitlines()
    total = 0
    for tree in trees:
        size, counts = tree.split(":")

        l, w = map(int, size.split("x"))
        counts = sum(map(int, counts.split()))

        if (l // 3) * (w // 3) >= counts:
            total += 1

    return total


def part2(puzzle: str): ...


def main():
    with open(f"../data/{day}/sample.txt", "r") as f:
        sample = f.read().strip()
    with open(f"../data/{day}/input.txt", "r") as f:
        input = f.read().strip()

    print(f"{'='*60}")
    print("Part 1")
    if SAMPLE:
        print(part1(sample))
    if PUZZLE:
        print(part1(input))

    print(f"{'='*60}")
    print("Part 2")
    if SAMPLE:
        print(part2(sample))
    if PUZZLE:
        print(part2(input))


if __name__ == "__main__":
    main()

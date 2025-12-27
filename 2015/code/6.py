import os
import numpy as np
import re

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    pattern = "\d+,\d+"
    lights = np.zeros((1000, 1000), dtype=bool)
    for line in puzzle.splitlines():
        p1, p2 = map(lambda x: x.split(","), re.findall(pattern, line))
        (r1, c1), (r2, c2) = map(int, p1), map(int, p2)
        if line.startswith("turn on"):
            # turn on by or with true
            lights[r1 : r2 + 1, c1 : c2 + 1] = True
        elif line.startswith("turn off"):
            # turn off by and with false
            lights[r1 : r2 + 1, c1 : c2 + 1] = False
        else:
            # toggle by exclusive or
            lights[r1 : r2 + 1, c1 : c2 + 1] ^= True

    return np.sum(lights)


def part2(puzzle: str):
    pattern = "\d+,\d+"
    lights = np.zeros((1000, 1000), dtype=int)
    for line in puzzle.splitlines():
        p1, p2 = map(lambda x: x.split(","), re.findall(pattern, line))
        (r1, c1), (r2, c2) = map(int, p1), map(int, p2)
        if line.startswith("turn on"):
            # turn on by or with true
            lights[r1 : r2 + 1, c1 : c2 + 1] += 1
        elif line.startswith("turn off"):
            # turn off by and with false
            lights[r1 : r2 + 1, c1 : c2 + 1] -= 1
            lights[lights < 0] = 0
        else:
            # toggle by exclusive or
            lights[r1 : r2 + 1, c1 : c2 + 1] += 2

    return np.sum(lights)


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

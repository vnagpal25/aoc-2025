import os
from collections import deque
from functools import cache

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    graph = {
        line.split(":")[0]: line.split(":")[1].split() for line in puzzle.splitlines()
    }

    total = 0
    # bfs
    q = deque(["you"])
    while q:
        node = q.popleft()
        if node == "out":
            total += 1
            continue
        for n in graph[node]:
            q.append(n)
    return total


def part2(puzzle: str):
    graph = {
        line.split(":")[0]: line.split(":")[1].split() for line in puzzle.splitlines()
    }

    @cache
    def count_paths(a, b):
        # only one path from a to b, trivially
        if a == b:
            return 1
        # sum all of the path counts from a's neighbors to b
        return sum(count_paths(n, b) for n in graph.get(a, []))

    # to get the number of paths from A to B through C
    # we multiply count(A, C) * count(C, B)
    # we can either go from fft to dac or dac to fft
    path_type_1 = (
        count_paths("svr", "fft")
        * count_paths("fft", "dac")
        * count_paths("dac", "out")
    )
    path_type_2 = (
        count_paths("svr", "dac")
        * count_paths("dac", "fft")
        * count_paths("fft", "out")
    )
    return path_type_1 + path_type_2


def main():
    with open(f"../data/{day}/sample.txt", "r") as f:
        sample = f.read().strip()
    with open(f"../data/{day}/sample2.txt", "r") as f:
        sample2 = f.read().strip()
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
        print(part2(sample2))
    if PUZZLE:
        print(part2(input))


if __name__ == "__main__":
    main()

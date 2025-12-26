from typing import List
day: str = "02"

test: str = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
pt1_ans: int = 2
pt2_ans: int = 4


def parse_input(string: str):
    # split lines by \n and split each line by space and convert each element to an int
    return list(map(lambda line: list(map(int, line.split())), string.splitlines()))


def safe(levels):
    # list of differences between each element
    diffs = [x - y for x, y in zip(levels, levels[1:])]
    return all(1 <= x <= 3 for x in diffs) or all(-3 <= x <= -1 for x in diffs)


def pt1(puzzle: List[int]):
    return len(list(filter(safe, puzzle)))


def pt2(puzzle):
    count = 0
    # check if any of the resulting lists from removing an arbitrary element are safe
    for levels in puzzle:
        if any(safe(levels[:i] + levels[i+1:]) for i in range(len(levels))):
            count += 1
    return count


def main(puzzle: str):
    global test
    test = parse_input(test)
    puzzle = parse_input(puzzle)
    assert pt1_ans == pt1(test)

    print(f"Part 1: {pt1(puzzle)}")

    assert pt2_ans == pt2(test)
    print(f"Part 2: {pt2(puzzle)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

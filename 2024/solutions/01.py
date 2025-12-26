from typing import List
day: str = "01"

test: str = """3   4
4   3
2   5
1   3
3   9
3   3
"""
pt1_ans: int = 11
pt2_ans: int = 31


def parse_input(string: str):
    # split by newline and also split each line by space and convert to int
    lines = list(map(lambda line: list(map(lambda x: int(
        x), line.split())), string.splitlines()))

    # return all first elements as a list and all second elements as a list
    return tuple(map(list, zip(*lines)))


def pt1(left_list: List[int], right_list: List[int]):
    left_list.sort(), right_list.sort()
    return sum((abs(a - b) for a, b in zip(left_list, right_list)))


def pt2(left_list: List[int], right_list: List[int]):
    return sum(el * right_list.count(el) for el in left_list)


def main(puzzle_input: str):
    global test
    test_left_list, test_right_list = parse_input(test)
    assert pt1_ans == pt1(test_left_list, test_right_list)
    left_list, right_list = parse_input(puzzle_input)
    print(f'Part 1: {pt1(left_list, right_list)}')

    assert pt2_ans == pt2(test_left_list, test_right_list)
    print(f'Part 2: {pt2(left_list, right_list)}')


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle_input = f.read()
        main(puzzle_input)

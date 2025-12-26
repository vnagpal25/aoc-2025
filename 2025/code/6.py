import os
import math

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    puzzle = puzzle.strip().splitlines()
    operators = puzzle[-1].split()
    numbers = list(map(str.split, puzzle[:-1]))
    operands = list(zip(*numbers))

    total = 0

    for nums, op in zip(operands, operators):
        nums = map(int, nums)
        if op == "*":
            total += math.prod(nums)
        elif op == "+":
            total += sum(nums)

    return total


def part2(puzzle: str):
    puzzle = puzzle.splitlines()
    # numbers = list(map(str.split, puzzle[:-1]))
    
    # get all columns
    columns = list(zip(*puzzle))
    groups = []
    group = []
    for col in columns:
        if set(col) == {" "}:
            groups.append(group)
            group = []
        else:
            group.append(col)
    groups.append(group)
    total = 0

    for group in groups:
        op = group[0][-1]
        equation = op.join(''.join(number[:-1]) for number in group)
        total += eval(equation)

    return total

def main():
    with open(f"../data/{day}/sample.txt", "r") as f:
        sample = f.read()
    with open(f"../data/{day}/input.txt", "r") as f:
        input = f.read()

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

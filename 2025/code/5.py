import os

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    ranges, ingredients = puzzle.split("\n\n")
    ranges = sorted(
        [tuple(map(int, range_.split("-"))) for range_ in ranges.split("\n")]
    )
    ingredients = list(map(int, ingredients.split("\n")))

    total = 0
    for ing in ingredients:
        for start, end in ranges:
            if start <= ing <= end:
                total += 1
                break

    return total


def part2(puzzle: str):
    ranges, _ = puzzle.split("\n\n")

    # sort the ranges by their starting value
    ranges = sorted(
        [tuple(map(int, range_.split("-"))) for range_ in ranges.split("\n")]
    )

    # merge intervals to be nonoverlapping
    non_overlapping = [ranges[0]]

    for curr_start, curr_end in ranges[1:]:
        last = non_overlapping[-1]

        # if the current interval starts before the last one ends
        # we pop the last one
        # update the starting and ending point point of the current interval
        if curr_start <= last[1]:
            non_overlapping.pop()

            # last one starts before because it was sorted
            curr_start = last[0]

            # current one might end before the last one, so we take the maximum
            curr_end = max(curr_end, last[1])

        # append new interval
        non_overlapping.append((curr_start, curr_end))

    # then we take the sum of the lengths of the intervals
    return sum(y - x + 1 for x, y in non_overlapping)


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

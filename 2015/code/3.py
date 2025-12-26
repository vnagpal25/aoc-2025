import os

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    x, y = 0, 0
    houses = {(x, y)}
    for char in puzzle:
        if char == ">":
            x += 1
        elif char == "<":
            x -= 1
        elif char == "^":
            y += 1
        elif char == "v":
            y -= 1
        houses.add((x, y))
    return len(houses)


def part2(puzzle: str):
    x1, y1, x2, y2 = 0, 0, 0, 0
    houses = {(x1, y1)}
    even = True
    for char in puzzle:
        if even:
            x, y = x1, y1
        else:
            x, y = x2, y2

        if char == ">":
            x += 1
        elif char == "<":
            x -= 1
        elif char == "^":
            y += 1
        elif char == "v":
            y -= 1
        houses.add((x, y))

        if even:
            x1, y1 = x, y
        else:
            x2, y2 = x, y

        even = not even

    return len(houses)


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

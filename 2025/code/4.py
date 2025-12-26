import os

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    grid = [
        [0] + [1 if char == "@" else 0 for char in string] + [0]
        for string in puzzle.splitlines()
    ]
    grid = [[0] * len(grid[0])] + grid + [[0] * len(grid[0])]
    accessible = 0

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            # if no roll in the cell
            if not cell:
                continue
            # sum eight adjacent
            tot = (
                sum(grid[i + di][j + dj] for di in (-1, 0, 1) for dj in (-1, 0, 1)) - 1
            )
            if tot < 4:
                accessible += 1
    return accessible


def part2(puzzle: str):
    grid = [
        [0] + [1 if char == "@" else 0 for char in string] + [0]
        for string in puzzle.splitlines()
    ]
    grid = [[0] * len(grid[0])] + grid + [[0] * len(grid[0])]

    can_remove = True
    total_accessible = 0
    while can_remove:
        accessible = 0
        removeable_squares = []
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                # if no roll in the cell
                if not cell:
                    continue
                # sum eight adjacent
                tot = (
                    sum(grid[i + di][j + dj] for di in (-1, 0, 1) for dj in (-1, 0, 1))
                    - 1
                )
                if tot < 4:
                    removeable_squares.append((i, j))
                    accessible += 1

        for i, j in removeable_squares:
            grid[i][j] = 0

        can_remove = bool(accessible)
        total_accessible += accessible

    return total_accessible


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

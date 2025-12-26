from typing import List
day: str = "04"

test: str = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
pt1_ans: int = 18
pt2_ans: int = 9


def pt1(grid: List[str]) -> int:
    total = 0

    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch != 'X':
                continue
            # N, S, E, W, NE, SE, NW, SW
            for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (-1, -1), (1, -1)]:
                if (dr, dc) == (0, 0):
                    continue
                if not 0 <= (i + 3 * dr) < len(grid) or not 0 <= (j + 3 * dc) < len(row):
                    continue

                # check if rest is a match
                if grid[i+dr][j+dc] == 'M' and grid[i+2*dr][j+2*dc] == 'A' and grid[i+3*dr][j+3*dc] == 'S':
                    total += 1

    return total


def pt2(grid) -> int:
    total = 0
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch != 'A':
                continue

            cont = False
            for dr, dc in [(-1, 1), (1, 1), (1, -1), (-1, -1)]:
                if not 0 <= i + dr < len(grid) or not 0 <= j+dc < len(row):
                    cont = True
            if cont:
                continue
            # Check NW to SE slash
            if (grid[i-1][j-1] == 'M' and grid[i+1][j+1] == 'S') or (grid[i-1][j-1] == 'S' and grid[i+1][j+1] == 'M'):
                # NE to SW slash
                if (grid[i-1][j+1] == 'M' and grid[i+1][j-1] == 'S') or (grid[i-1][j+1] == 'S' and grid[i+1][j-1] == 'M'):
                    total += 1
    return total


def main(puzzle: str) -> None:
    global test
    test = test.splitlines()
    puzzle = puzzle.splitlines()

    assert pt1_ans == pt1(test)
    print(f"Part 1: {pt1(puzzle)}")

    assert pt2_ans == pt2(test)
    print(f"Part 2: {pt2(puzzle)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

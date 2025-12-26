from typing import List, Tuple
import os
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
pt1_ans: int = 41
pt2_ans: int = 6


def parse_input(string: str) -> List[str]:
    grid = string.splitlines()
    start_pos,  = [(i, j) for i, row in enumerate(grid)
                   for j, ch in enumerate(row) if ch == '^']
    return grid, start_pos


def pt1(grid: List[str], start: Tuple[int]):
    visited = {start}
    r, c = start
    dr, dc = -1, 0

    while True:
        visited.add((r, c))
        if not 0 <= r+dr < len(grid) or not 0 <= c + dc < len(grid[r]):
            break
        elif grid[r+dr][c+dc] == '#':
            # turn 90 degrees
            dr, dc = dc, -dr
        else:
            r, c = r + dr, c + dc

    # print('\n'.join([''.join(['X' if (i, j) in visited else ch for j, ch in enumerate(row)])
    #       for i, row in enumerate(grid)]))
    return len(visited)


def pt2(grid: List[str], start):
    def loops(grid_, start_):
        visited = set()
        r, c = start_
        dr, dc = -1, 0

        while True:
            # we track direction as well, guard could be moving across same location but not in the same
            visited.add((r, c, dr, dc))
            if not 0 <= r+dr < len(grid_) or not 0 <= c + dc < len(grid_[r]):
                return False
            if grid_[r+dr][c+dc] == '#':
                # turn 90 degrees
                dr, dc = dc, -dr
            else:
                # move along
                r, c = r + dr, c + dc
            # same position and orientation has been visited before
            if (r, c, dr, dc) in visited:
                return True
    total = 0
    grid = [list(row) for row in grid]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != '.':
                continue
            grid[i][j] = '#'
            if loops(grid, start):
                total += 1
            grid[i][j] = '.'
    return total


def main(puzzle: str):
    test_grid, test_start = parse_input(test)
    grid, start = parse_input(puzzle)

    assert pt1_ans == pt1(test_grid, test_start)
    print(f"Part 1: {pt1(grid, start)}")

    assert pt2_ans == pt2(test_grid, test_start)
    print(f"Part 2: {pt2(grid, start)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

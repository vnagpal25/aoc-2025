import os
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
pt1_ans: int = 14
pt2_ans: int = 34


def parse_input(string: str):
    grid = string.splitlines()
    locs = {}
    for antenna in set(char for char in list(''.join(grid)) if char != '.'):
        locs[antenna] = [(i, j) for i, line in enumerate(grid)
                         for j, ch in enumerate(line) if ch == antenna]

    return grid, locs


def pt1(grid, locs):
    antinodes = set()  # ensures uniqueness
    for antenna_locs in locs.values():
        """
        find all the antinodes for all locations of antenna type
        ideally if we have n atennae, then we have n(n-1) possible antinode locations (Think of this as every atenna having an antinode with each antenna)
        however, this may not always be in the grid or even unique
        """
        if len(locs) == 1:  # lone antenna won't have any antinodes
            continue
        # generate all n(n-1) pairs of locations
        pairs = [(loc1, loc2)
                 for loc1 in antenna_locs for loc2 in antenna_locs if loc1 != loc2]

        # for each pair of locations, we find the antinode on the other side of the second antenna
        for loc1, loc2 in pairs:
            (i1, j1), (i2, j2) = loc1, loc2
            i3, j3 = i1 + 2*(i2 - i1), j1 + 2*(j2 - j1)
            # we consider it only if its in bounds
            if 0 <= i3 < len(grid) and 0 <= j3 < len(grid[0]):
                antinodes.add((i3, j3))
    return len(antinodes)


def pt2(grid, locs):
    antinodes = set()  # ensures uniqueness
    for antenna_locs in locs.values():
        # find all the antinodes for all locations of antenna type
        # ideally if we have n atennae, then we have n(n-1) possible antinode locations (Think of this as every atenna having an antinode with each antenna)
        # however, this may not always be in the grid or even unique
        if len(locs) == 1:  # lone antenna won't have any antinodes
            continue
        # generate all n(n-1) pairs of locations
        pairs = [(loc1, loc2)
                 for loc1 in antenna_locs for loc2 in antenna_locs if loc1 != loc2]
        # for each pair of antenna, we extend the line of antennae on the other side of the second attennae and stop counting once we go out of bounds
        for loc1, loc2 in pairs:
            (i1, j1), (i2, j2) = loc1, loc2
            antinodes.add((i1, j1))
            antinodes.add((i2, j2))
            di, dj = i2-i1, j2-j1
            while True:
                i3, j3 = i1 + 2*di, j1 + 2*dj
                if 0 <= i3 < len(grid) and 0 <= j3 < len(grid[0]):
                    antinodes.add((i3, j3))
                else:
                    break
                (i1, j1), (i2, j2) = (i2, j2), (i3, j3)

    return len(antinodes)


def main(puzzle: str):
    test_grid, test_locs = parse_input(test)
    grid, locs = parse_input(puzzle)

    assert pt1_ans == pt1(test_grid, test_locs)
    print(f"Part 1: {pt1(grid,locs)}")

    assert pt2_ans == pt2(test_grid, test_locs)
    print(f"Part 2: {pt2(grid,locs)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

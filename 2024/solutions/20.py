import os
from collections import deque
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

pt1_ans: int = 0
pt2_ans: int = 0


def parse_input(string: str):
    grid = [list(line) for line in string.strip().splitlines()]
    return grid


def populate_distances(grid):
    # breadth-first fill populate the distances grid to get the distance of each node from the start node

    # starting position
    (r, c),  = [(r, c) for r, row in enumerate(grid)
                for c, ch in enumerate(row) if ch == 'S']

    # initialize all distances as -1, and 0 for the starting position
    distances = [[-1] * len(grid[0]) for _ in grid]
    distances[r][c] = 0

    # initialize queue with starting position and traverse all explorable nodes
    queue = deque([(r, c)])
    while queue:
        # explore all directions
        cr, cc = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            nr, nc = cr + dr, cc + dc
            # is out of bounds or is wall
            if not 0 <= nr < len(grid) or not 0 <= nc < len(grid[0]) or grid[nr][nc] == '#':
                continue

            # we've already seen this node before
            if distances[nr][nc] != -1:
                continue

            # it takes one more move to get to this node
            distances[nr][nc] = distances[cr][cc] + 1

            # explore later
            queue.append((nr, nc))

    return distances


def pt1(grid):
    # get distances of each node from starting node
    distances = populate_distances(grid)

    count = 0
    for r, row in enumerate(distances):
        for c, ch in enumerate(row):
            if ch == -1:  # wall
                continue

            # 4 cheating positions (NE, E, SE, S)
            # other 4 positions will be explored at other nodes
            for dr, dc in [(-1, 1), (0, 2), (1, 1), (2, 0)]:
                nr, nc = r + dr, c + dc

                # out of bounds
                if not 0 <= nr < len(grid) or not 0 <= nc < len(grid[0]):
                    continue

                # must not be a wall, note that pieces in between can be walls, but ending and start can't be walls
                if distances[nr][nc] == -1:
                    continue

                # 102 because, we're spending 2 seconds cheating
                # so the existing path needs to be 102 to save 100 seconds
                if abs(distances[r][c] - distances[nr][nc]) >= 102:
                    count += 1

    return count


def pt2(grid):
    distances = populate_distances(grid)

    count = 0
    for r, row in enumerate(distances):
        for c, ch in enumerate(row):
            if ch == -1:  # wall
                continue
            # we can cheat from 2 to 20 picoseconds, inclusive
            for cheat_length in range(2, 21):
                # pdr can go from 0 to cheat_length inclusive
                for pdr in range(cheat_length + 1):
                    # pdr and pdc sum to cheat length
                    pdc = cheat_length - pdr

                    # we essentially have all positive values of dr and dc that sum up to our cheat length
                    # similar to a negative sloped line in the first quadran
                    # we need to get dr and dc in all 4 quadrants
                    # we use a set, because if either pdr or pdc are 0, we'll have duplicates
                    for dr, dc in {(pdr, pdc), (pdr, -pdc), (-pdr, -pdc), (-pdr, pdc)}:
                        nr, nc = r + dr, c + dc

                        # out of bounds
                        if not 0 <= nr < len(grid) or not 0 <= nc < len(grid[0]):
                            continue

                        # must not be a wall, note that pieces in between can be walls, but ending and start can't be walls
                        if distances[nr][nc] == -1:
                            continue

                        # 100 + cheat length because, we're spending cheat_length seconds cheating
                        # so the existing path needs to be at least 100 + cheat_length
                        # to save at least 100 seconds
                        if distances[r][c] - distances[nr][nc] >= 100 + cheat_length:
                            count += 1

    return count


def main(puzzle: str):
    grid = parse_input(puzzle)

    print(f"Part 1: {pt1(grid)}")
    print(f"Part 2: {pt2(grid)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

import os
from collections import deque
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
pt1_ans: int = 36
pt2_ans: int = 81


def parse_input(string: str):
    park = string.splitlines()
    trailheads = [(i, j) for i, row in enumerate(park)
                  for j, ch in enumerate(row) if ch == '0']
    return park, trailheads


def pt1(park, trailheads):
    def hike(trailhead):
        """Hike from the beginning of the trailhead, one level at a time and count the number of unique apexes which are reachable"""
        # queue of paths to explore, starting with trailhead at level 0
        q = deque([(trailhead, 0)])
        apexes = set()  # keeps track of unique apex points
        score = 0  # to return

        # explore all possible paths
        while q:
            # get current location and level
            (r, c), level = q.popleft()

            # we've reached the max level, no more need to explore the current trail
            if level == 9:
                # unreached apex, add to visited and increment score
                if (r, c) not in apexes:
                    apexes.add((r, c))
                    score += 1
                continue

            # check all cardinal directions of trail (N, W, E, S)
            for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                # out of bounds ==> disregard
                if not 0 <= r+dr < len(park) or not 0 <= c + dc < len(park[r]):
                    continue
                # keep exploring the trail if there is a one level up path
                if int(park[r+dr][c+dc]) == level + 1:
                    q.append(((r+dr, c+dc), level+1))
        return score

    return sum(hike(trailhead) for trailhead in trailheads)


def pt2(park, trailheads):
    def hike(trailhead):
        """Hike from the beginning of the trailhead, one level at a time and count the number of unique paths to an apex"""
        # queue of path points to explore, current path and trailhead at level 0
        q = deque([(trailhead, [trailhead], 0)])
        visited_paths = set()  # keeps track of all of the visited paths
        score = 0  # to return

        # explore all possible path points
        while q:
            # get current location, current path, and level
            (r, c), path, level = q.popleft()

            # we've reached the max level, no more need to explore the current trail
            if level == 9:
                # check if this path was taken before
                if tuple(path) not in visited_paths:
                    score += 1
                visited_paths.add(tuple(path))
                continue

            # check all cardinal directions of trail (N, W, E, S)
            for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                # out of bounds ==> disregard
                if not 0 <= r+dr < len(park) or not 0 <= c + dc < len(park[r]):
                    continue

                # keep exploring the trail if there is a one level up point
                if int(park[r+dr][c+dc]) == level + 1:
                    # make copy of path list and append new location
                    path_copy = path.copy()
                    path_copy.append((r+dr, c+dc))

                    # explore later
                    q.append(((r+dr, c+dc), path_copy, level+1))

        return score
    return sum(hike(trailhead) for trailhead in trailheads)


def main(puzzle: str):
    test_park, test_heads = parse_input(test)
    park, trailheads = parse_input(puzzle)

    assert pt1_ans == pt1(test_park, test_heads)
    print(f"Part 1: {pt1(park, trailheads)}")

    assert pt2_ans == pt2(test_park, test_heads)
    print(f"Part 2: {pt2(park, trailheads)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

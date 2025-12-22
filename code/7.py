import os
from collections import deque
from functools import cache

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    puzzle = [list(row) for row in puzzle.splitlines()]
    m, n = len(puzzle), len(puzzle[0])

    (start,) = [(r, c) for r in range(m) for c in range(n) if puzzle[r][c] == "S"]

    beams = deque([start])
    beam_set = set(start)
    split_count = 0

    while beams:
        r, c = beams.popleft()

        # move downward
        nr, nc = r + 1, c

        # check out of bounds
        if not (0 <= nr < m and 0 <= nc < n) or (nr, nc) in beam_set:
            continue
        if puzzle[nr][nc] == "^":
            # split beam
            lc, rc = nc - 1, nc + 1
            split_count += 1
            # print(f"Splitting at {nr, nc}")
            if 0 <= lc < n:
                beams.append((nr, lc))
                beam_set.add((nr, lc))
            if 0 <= rc < n:
                beams.append((nr, rc))
                beam_set.add((nr, rc))
        else:
            beams.append((nr, nc))
            beam_set.add((nr, nc))

    return split_count


def part2(puzzle: str):
    puzzle = [list(row) for row in puzzle.splitlines()]
    m, n = len(puzzle), len(puzzle[0])

    (start,) = [(r, c) for r in range(m) for c in range(n) if puzzle[r][c] == "S"]

    # instead of BFS, we'll do a DFS+Cache approach
    # top down DP
    @cache
    def get_num_paths(r, c):
        if r >= m:
            # we've reached the bottom
            return 1
        elif puzzle[r][c] != "^":
            # pass the beam through
            return get_num_paths(r + 1, c)
        else:
            # split so we count the number of paths on the left and the right
            return get_num_paths(r, c - 1) + get_num_paths(r, c + 1)

    return get_num_paths(*start)


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

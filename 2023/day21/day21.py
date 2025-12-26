from collections import deque
import sys
file = sys.argv[1]

with open(file, 'r') as f:
    grid = f.read().splitlines()
    assert len(grid) == len(grid[0])  # grid must be square
    size = len(grid)


def fill(start_row, start_col, num_steps):
    ans = set()  # contains all reachable nodes
    seen = {(start_row, start_col)}  # contains all seen nodes
    # queue for traversing grid in BFS fill fashion
    q = deque([(start_row, start_col, num_steps)])

    # BFS fill for traversing grid, starting at start_row, start_col
    while q:
        # current row, col, and num of steps remaining
        r, c, s = q.popleft()
        if s % 2 == 0:  # if we have an even amount of steps remaining, we can trivially move from this space to another space to exhaust our steps to 0, therefore, this is a valid reachable state
            ans.add((r, c))

        # no more steps remaining
        if s == 0:
            continue

        # N, S, E, W cardinal directions
        for nr, nc in [(r - 1, c), (r + 1, c), (r, c + 1), (r, c - 1)]:
            # invalid conditions
            # not_on_grid, on rock, visited
            if nr < 0 or nr >= size or nc < 0 or nc >= size or grid[nr][nc] == '#' or (nr, nc) in seen:
                continue  # we skip this space
            # add the following space to the seen set, and append it to our queue with 1 less step
            seen.add((nr, nc))
            q.append((nr, nc, s - 1))

    return len(ans)


def main():
    # extract the starting row and starting column
    start_row, start_col = next((r, c) for r, row in enumerate(grid)
                                for c, ch in enumerate(row) if ch == "S")
    # starting position is directly in the middle of the odd sized grid

    """Part 1"""
    # print(fill(start_row, start_col, 64))

    """Part 2"""
    num_steps = 26501365
    assert start_row == start_col == (size//2)
    assert num_steps % size == size // 2
    # number of repeating grids to in any cardinal direction from the starting grid
    mega_grid_width = num_steps // size - 1
    num_odd_grids = (mega_grid_width // 2 * 2 + 1) ** 2
    num_even_grids = ((mega_grid_width + 1) // 2 * 2) ** 2
    print(num_even_grids, num_odd_grids)

    odd_points = fill(start_row, start_col, size * 2 + 1)
    even_points = fill(start_row, start_col, size * 2)

    # corner grids which can't be entirely traversed
    corner_t = fill(size - 1, start_col, size - 1)
    corner_r = fill(start_row, 0, size - 1)
    corner_b = fill(0, start_col, size - 1)
    corner_l = fill(start_row, size - 1, size - 1)

    small_tr = fill(size-1, 0, size // 2 - 1)
    small_tl = fill(size - 1, size - 1, size // 2 - 1)
    small_br = fill(0, 0, size // 2 - 1)
    small_bl = fill(0, size - 1, size // 2 - 1)

    large_tr = fill(size-1, 0, size * 3 // 2 - 1)
    large_tl = fill(size - 1, size - 1, size * 3 // 2 - 1)
    large_br = fill(0, 0, size * 3 // 2 - 1)
    large_bl = fill(0, size - 1, size * 3 // 2 - 1)
    print(num_odd_grids * odd_points +
          num_even_grids * even_points +
          corner_t + corner_r +
          corner_b + corner_l +
          (mega_grid_width + 1) * (small_tr + small_tl + small_br + small_bl) +
          mega_grid_width * (large_tr + large_tl + large_br + large_bl))


if __name__ == '__main__':
    main()

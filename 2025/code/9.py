import os
from collections import deque

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    coords = [tuple(map(int, coord.split(","))) for coord in puzzle.splitlines()]

    max_area = float("-inf")
    for i in range(len(coords)):
        x1, y1 = coords[i]
        for j in range(i + 1, len(coords)):
            x2, y2 = coords[j]
            max_area = max(max_area, (1 + abs(x1 - x2)) * (1 + abs(y1 - y2)))

    return max_area


def part2(puzzle: str):
    points = [tuple(map(int, coord.split(","))) for coord in puzzle.splitlines()]

    # unique x and y locations in ascending order
    xs = sorted({x for x, _ in points})
    ys = sorted({y for _, y in points})

    # we want to encode the amount of free space between each of the coordinates
    # along each axis independently
    x_sizes, y_sizes = {}, {}

    for i, (x1, x2) in enumerate(zip(xs, xs[1:])):
        # 2i + 1 because we want to encode free space in the odd indices
        # and red tiles in even indices
        x_sizes[2 * i + 1] = x2 - x1 - 1

    for i, (y1, y2) in enumerate(zip(ys, ys[1:])):
        y_sizes[2 * i + 1] = y2 - y1 - 1

    # 2z - 1 because each tile will have a column of space except the last column
    grid = [[0] * (2 * len(ys) - 1) for _ in range(2 * len(xs) - 1)]

    # fill grid with 1s with red and green tiles
    for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
        # for each point x1, y1 we grab the next point x2, y2

        # red tiles in even indices
        cx1, cx2 = sorted([xs.index(x1) * 2, xs.index(x2) * 2])
        cy1, cy2 = sorted([ys.index(y1) * 2, ys.index(y2) * 2])

        # all tiles in between red tiles are green
        # we encode all colored tiles as 1

        # horizontal
        if cx1 == cx2:
            for cy in range(cy1, cy2 + 1):
                grid[cx1][cy] = 1
        # vertical
        else:
            for cx in range(cx1, cx2 + 1):
                grid[cx][cy1] = 1

    # now we need to fill in the tiles that are within the boundary
    # the easiest way to figure out which tiles are within is to do a bfs fill
    # from the outside of the boundary to determine which points are not inside
    out = {(-1, -1)}  # left most point outside (functions as buffer)
    q = deque(out)

    while q:
        curr_x, curr_y = q.popleft()

        for nx, ny in [
            (curr_x - 1, curr_y),
            (curr_x + 1, curr_y),
            (curr_x, curr_y - 1),
            (curr_x, curr_y + 1),
        ]:
            # needs to be within buffer
            if not (-1 <= nx <= len(grid) and -1 <= ny <= len(grid[0])):
                continue

            # within boundary but on tile wall
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny]:
                continue

            # already marked as an external point
            if (nx, ny) in out:
                continue

            # note this includes the -1 indexed points, but we'll handle this
            out.add((nx, ny))
            q.append((nx, ny))

    # mark internal tiles as colored
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if (x, y) in out:
                continue
            # mark all internal points as 1
            grid[x][y] = 1

    # construct a prefix sum array (psa)
    # based on grid values
    psa = [[0] * len(row) for row in grid]

    for x in range(len(psa)):
        for y in range(len(psa[x])):
            left = psa[x - 1][y] if x else 0
            top = psa[x][y - 1] if y else 0
            topleft = psa[x - 1][y - 1] if x and y else 0
            # subtract topleft since it will be double counted
            psa[x][y] = grid[x][y] + left + top - topleft

    def valid(x1, y1, x2, y2):
        # get compressed coordinates
        cx1, cx2 = sorted([xs.index(x1) * 2, xs.index(x2) * 2])
        cy1, cy2 = sorted([ys.index(y1) * 2, ys.index(y2) * 2])

        left = psa[cx1 - 1][cy2] if cx1 else 0  # area of left portion
        top = psa[cx2][cy1 - 1] if cy1 else 0  # area of top portion
        topleft = psa[cx1 - 1][cy1 - 1] if cx1 and cy1 else 0  # topleft portion

        # subtract left and top and add topleft because of double counting
        # this gives us the number of 1s between x1 y1 and x2 y2
        count = psa[cx2][cy2] - left - top + topleft

        # to be a valid rectangle it must not contain any 0s (uncolored tiles)
        # thus it must simply be the area of the rectangle formed by the 2 points
        return count == (cx2 - cx1 + 1) * (cy2 - cy1 + 1)

    max_area = float("-inf")
    for i, (x1, y1) in enumerate(points):
        for x2, y2 in points[i + 1 :]:
            # disregard all invalid rectangles
            if not valid(x1, y1, x2, y2):
                continue

            max_area = max(max_area, (1 + abs(x1 - x2)) * (1 + abs(y1 - y2)))
    
    return max_area

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

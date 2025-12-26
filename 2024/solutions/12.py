import os
from collections import deque
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
pt1_ans: int = 1930
pt2_ans: int = 1206


def parse_input(string: str):
    plot = [list(line.strip()) for line in string.splitlines()]
    return plot


def get_regions(plot):
    regions = []  # list of sets (regions)
    seen = set()  # contains all visited plants

    # iterate over entire plot
    for i, row in enumerate(plot):
        for j, plant in enumerate(row):
            # already visited this plant, so continue
            if (i, j) in seen:
                continue

            # mark as visited
            seen.add((i, j))

            # initialize region set
            region = {(i, j)}

            # flood fill to determine the region
            q = deque([(i, j)])
            while q:
                # get position
                curr_i, curr_j = q.popleft()

                # cardinal directions (N, S, W, E)
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    # out of bounds, so continue
                    if not 0 <= curr_i+di < len(plot) or not 0 <= curr_j+dj < len(plot[0]):
                        continue

                    # not same plant, so not same region, so continue
                    if plot[curr_i + di][curr_j+dj] != plant:
                        continue

                    # already marked as a neighbor, so continue
                    if (curr_i + di, curr_j + dj) in region:
                        continue

                    # mark it as part of our region and append it to the queue for further exploration
                    region.add((curr_i + di, curr_j + dj))
                    q.append((curr_i + di, curr_j + dj))

            # mark whole region as seen and append it to our regions list
            seen |= region
            regions.append(region)

    return regions


def area(region):
    """area of a region is the number of plants in the region"""
    return len(region)


def pt1(plot):
    def perimeter(region):
        """calculate the perimeter of a region"""
        output = 0
        for r, c in region:
            output += 4  # maximum perimeter of a single plant
            for nr, nc in [(r + 1, c), (r - 1, c), (r, c+1), (r, c-1)]:
                # for each neighbor in region, we decrement
                if (nr, nc) in region:
                    output -= 1
        return output

    regions = get_regions(plot)

    return sum(area (region) * perimeter(region) for region in regions)


def pt2(plot):
    def side_count(region):
        """count the number of sides of a region"""

        # get all of the edge coordinates and their orientation (l, r, u, d) that they face in
        edges = {}
        for r, c in region:
            for nr, nc in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]:
                if (nr, nc) in region:
                    # that direction is not an outward edge, so ignore
                    continue
                # get the coordinates of the edge as the average of the two squares
                er, ec = (r + nr) / 2, (c + nc) / 2

                # assign the edge an orientation of left, right, down or up
                edges[(er, ec)] = (er - r, ec - c)

        # piece together all edges
        # 2 edges are of the same side if they are adjacent and facing the same direction
        explored = set()
        side_count = 0
        for edge, direction in edges.items():
            if edge in explored:
                # we have already explored this edge so ignore
                continue

            # mark this edge as visited, and increment side count because we are on a new side
            explored.add(edge)
            side_count += 1

            # position of edge in plot
            er, ec = edge
            if er % 1 == 0:
                # this is a vertical edge so we need to explore up and down
                for dr in (-1, 1):
                    cr = er + dr
                    # checks if adjacent edge exists and has the same direction
                    # mark as explored and keep going in that direction
                    while edges.get((cr, ec)) == direction:
                        explored.add((cr, ec))
                        cr += dr
            elif ec % 1 == 0:
                # this is a horizontal edge so we need to explore left and right
                for dc in (-1, 1):
                    cc = ec + dc
                    # checks if adjacent edge exists and has the same direction
                    while edges.get((er, cc)) == direction:
                        explored.add((er, cc))
                        cc += dc
        return side_count

    regions = get_regions(plot)

    return sum(area(region) * side_count(region) for region in regions)


def main(puzzle: str):
    test_plot = parse_input(test)
    plot = parse_input(puzzle)

    assert pt1_ans == pt1(test_plot)
    print(f"Part 1: {pt1(plot)}")

    assert pt2_ans == pt2(test_plot)
    print(f"Part 2: {pt2(plot)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

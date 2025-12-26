import os
from heapq import heappush, heappop
from typing import List, Tuple, Set, Dict
from tqdm import tqdm
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""
pt1_ans: int = 22
pt2_ans: Tuple[int, int] = (6, 1)


def parse_input(string: str, grid_size: int):
    grid = [['.' for i in range(grid_size)] for i in range(grid_size)]
    coords = [tuple(map(int, coord_string.split(',')))
              for coord_string in string.splitlines()]
    return grid, coords


def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """
    Calculate Manhattan distance between two points. 
    This will serve as the A* heuristic.
    We note that this heuristic is ~admissible~ as it never overestimates true cost
    because manhattan distance would be optimal cost if there were no barriers.

    We note that this heuristic is also ~consistent~ because it satisfies the triangle inequality in our use case.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_neighbors(pos: Tuple[int, int], grid: List[List[str]]) -> List[Tuple[int, int]]:
    """Get valid neighboring nodes to the current node."""
    rows, cols = len(grid), len(grid[0])
    neighbors = []

    r, c = pos
    # Check all four directions (up, right, down, left)
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        # check boundary conditions and if the new square is a wall
        if not 0 <= nr < rows or not 0 <= nc < cols or grid[nr][nc] == '#':
            continue
        neighbors.append((nr, nc))

    return neighbors


def pt1(grid: List[List[str]], coords) -> int:
    """
    Implement A* algorithm to find shortest path from top-left to bottom-right.
    Returns (steps_taken, path) tuple.
    """
    rows, cols = len(grid), len(grid[0])
    start = (0, 0)

    # place corrupted bits in grid
    for x, y in coords:
        grid[y][x] = '#'

    goal = (rows-1, cols-1)  # goal is in bottom right corner of the grid

    # Priority queue for open set
    priority_queue = []
    heappush(priority_queue, (0, start))  # (f_score, position)

    # Track visited nodes as keys and their predecessor node as a value
    # will be used for backtracking the optimal path
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}

    # Cost from start to current node
    g_score: Dict[Tuple[int, int], int] = {start: 0}

    # Estimated total cost from start to goal through current node
    # f(start) = g(start) + h(start) = h(start)
    f_score: Dict[Tuple[int, int], int] = {
        start: manhattan_distance(start, goal)}

    while priority_queue:
        # Get node with lowest f_score
        _, current = heappop(priority_queue)

        # If we reached the goal
        if current == goal:
            # Reconstruct path
            path = []

            # append predecessors starting from goal state
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)  # start does not have a predecessor node
            path.reverse()  # reverse the path
            return len(path) - 1

        # Check all neighbors
        for neighbor in get_neighbors(current, grid):
            # Distance from start to neighbor through current
            neighbor_g_score = g_score[current] + 1

            # if neighbor is not in g_score, it means that we haven't tracked the optimal cost of reaching it yet
            # if the neighbor g score is lower than the previously tracked cost of it
            #
            # In either case, we
            #   (1) update the predecessor of the neighbor node as the current node
            #   (2) update the optimal cost of reaching it
            #   (3) update the f score of the neighbor (estimated cost of optimal path through neighbor)
            if neighbor not in g_score or neighbor_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = neighbor_g_score

                # f(n) = g(n) + h(n), heuristic is manhattan distance from neighbor to goal
                f_score[neighbor] = neighbor_g_score + \
                    manhattan_distance(neighbor, goal)

                # now we push neighbor with the estimated total cost to the priority queue
                heappush(priority_queue, (f_score[neighbor], neighbor))

    # No path found
    return -1


def pt2(grid: List[List[str]], coords) -> int:
    # Try corrupting no coords all the way up to all coords
    for i in tqdm(range(len(coords) + 1)):
        # path length is -1 if there is no path to the goal
        # so we return the coord that led to no solution
        if pt1(grid.copy(), coords[:i]) == -1:
            return coords[i-1]


def main(puzzle: str):
    test_grid, test_coords = parse_input(test, 7)
    grid, coords = parse_input(puzzle, 71)

    assert pt1_ans == pt1(test_grid.copy(), test_coords[:12])
    print(f"Part 1: {pt1(grid.copy(), coords[:1024])}")

    assert pt2_ans == pt2(test_grid.copy(), test_coords[12:])
    print(f"Part 2: {pt2(grid.copy(), coords[1024:])}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

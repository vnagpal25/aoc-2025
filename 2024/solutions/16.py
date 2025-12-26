import os
from collections import deque
import heapq
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test0: str = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
test1: str = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""
test0_pt1_ans: int = 7036
test1_pt1_ans: int = 11048
test0_pt2_ans: int = 45
test1_pt2_ans: int = 64


def parse_input(string: str):
    return [list(line) for line in string.splitlines()]


def pt1_bfs(maze):
    """BFS on the  maze to collect all of path sums. Incredibly inefficient"""
    def score(path):
        dirs = [(i2-i1, j2-j1) for (i1, j1), (i2, j2) in zip(path, path[1:])]
        num_steps = len(dirs)
        curr_dir = (0, 1)  # initially moving east
        turns = 0
        for dir in dirs:
            if dir != curr_dir:
                turns += 1
                curr_dir = dir
        return turns*1000 + num_steps

    # start state, goal state
    for i, row in enumerate(maze):
        for j, ch in enumerate(row):
            if ch == 'S':
                start = (i, j)
            elif ch == 'E':
                end = (i, j)

    # print('\n'.join([''.join(line) for line in maze]))

    q = deque([[start]])
    paths = set()  # tuples of coordinates for complete paths
    while q:
        print(len(q))
        curr_path = q.popleft()
        r, c = curr_path[-1]
        # we've reached the goal state, no need to explore further from this state
        if (r, c) == end:
            paths.add(tuple(curr_path))
            continue

        # cardinal exploration
        for nr, nc in [(r, c + 1), (r, c - 1), (r + 1, c), (r - 1, c)]:
            #
            # boundary conditions
            if not 0 <= nr < len(maze) or not 0 <= nc < len(maze[0]):
                continue
            char = maze[nr][nc]
            if char == '#':
                continue
            # no need to visit a previously visited square again
            if (nr, nc) in curr_path:
                continue
            path = list(curr_path)
            q.append(path + [(nr, nc)])

    return min(score(path) for path in paths)


def pt1(maze):
    """Dijkstra'ss on the  maze to collect all of path sums"""
    # find start state, goal state
    for i, row in enumerate(maze):
        for j, ch in enumerate(row):
            if ch == 'S':
                sr, sc = i, j
            elif ch == 'E':
                er, ec = i, j

    # priority queue is the key data structure in dijkstra's algorithm
    # we keep track of the cost to reach a particular node (which is the coordinates and orientation)
    # initial orientation is east whic is (0, 1)
    pq = [(0, sr, sc, 0, 1)]

    # keeps track of the cheapest way to visit a node by its position and orientation
    seen = {(sr, sc, 0, 1)}

    while pq:
        # we get the next cheapest node to visit from the priority queue
        # we also mark it as seen as this the cheapest way to get to this node
        # by default heappop treats list as a min heap compares 1st elements of the tuples
        cost, r, c, dr, dc = heapq.heappop(pq)
        seen.add((r, c, dr, dc))

        # this the goal state and by design, Dijkstra's algorithm first reaches with the lowest cost for the node being processed, so we return the cost
        if (r, c) == (er, ec):
            return cost

        # we can do three possible moves: move forward, turn left(counterclockwise) or turn right(clockwise)
        for new_cost, nr, nc, ndr, ndc in [(cost + 1, r + dr, c + dc, dr, dc),
                                           (cost + 1000, r, c, dc, -dr),
                                           (cost + 1000, r, c, -dc, dr)]:
            # out of the maze
            if not 0 <= nr < len(maze) or not 0 <= nc < len(maze[0]):
                continue

            char = maze[nr][nc]
            # running into a wall
            if char == '#':
                continue

            # we've been in this orientation and position before
            if (nr, nc, ndr, ndc) in seen:
                continue

            # add the new node to the priority queue
            heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))


def pt2(maze):
    """Dijkstra'ss on the  maze to collect all of path sums"""

    # finding start state, goal state
    for i, row in enumerate(maze):
        for j, ch in enumerate(row):
            if ch == 'S':
                sr, sc = i, j
            elif ch == 'E':
                er, ec = i, j

    # priorirty queue which is used to store best possible (lowest cost) next state that can be reached from current state
    pq = [(0, sr, sc, 0, 1)]

    # map which maps each state (r, c, dr, dc) to the lowest cost required to get there
    state_cost_map = {(sr, sc, 0, 1): 0}

    # map which maps each state s to all previous states that reach s on an optimal path to the end state
    backtrack = {}

    min_cost = float('inf')  # optimal cost to reach end state
    ending_states = set()  # all (r, c, dr, dc) that reach (er, ec) ending state

    # Dijkstra's Algorithm
    while pq:
        # get the cheapest next move we can make (greedy)
        cost, r, c, dr, dc = heapq.heappop(pq)

        # we've already reached this state for cheaper before, so we skip
        if cost > state_cost_map.get((r, c, dr, dc), float('inf')):
            continue
        # set new optimal cost
        state_cost_map[(r, c, dr, dc)] = cost

        # reached goal state
        if (r, c) == (er, ec):
            if cost > min_cost:  # we've already explored all the best ways to reach this state, so we break
                break
            # update best cost and add to end states
            min_cost = cost
            ending_states.add((r, c, dr, dc))

        # we can do three possible moves: move forward, turn left(counterclockwise) or turn right(clockwise)
        for new_cost, nr, nc, ndr, ndc in [(cost + 1, r + dr, c + dc, dr, dc),
                                           (cost + 1000, r, c, dc, -dr),
                                           (cost + 1000, r, c, -dc, dr)]:
            # out of the maze
            # boundary conditions
            if not 0 <= nr < len(maze) or not 0 <= nc < len(maze[0]):
                continue

            # running into a wall
            char = maze[nr][nc]
            if char == '#':
                continue

            # grab the best cost to reach this next state
            next_lowest_cost = state_cost_map.get(
                (nr, nc, ndr, ndc), float('inf'))

            # we've reached this state for cheaper, so we skip
            if new_cost > next_lowest_cost:
                continue
            # we found a more efficient path!
            elif new_cost < next_lowest_cost:
                # we renitialize it's previous nodes
                backtrack[(nr, nc, ndr, ndc)] = set()
                # and let's also update its best cost
                state_cost_map[(nr, nc, ndr, ndc)] = new_cost
            # add the current node as a previous node for the next node
            backtrack[(nr, nc, ndr, ndc)].add((r, c, dr, dc))
            # add the new node to the priority queue
            heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))

    # breadth first fill in order to determine all states which are in the optimal paths
    states = deque(ending_states)
    seen = set(ending_states)
    while states:
        key = states.popleft()
        for last in backtrack.get(key, []):
            if last in seen:
                continue
            seen.add(last)
            states.append(last)
    # seen now contains all states (r, c, dr, dc) that are in optimal paths
    # question only asks for (r, c) so we filter for uniqueness
    optimal_states = {(r, c) for r, c, _, _ in seen}
    return len(optimal_states)


def main(puzzle: str):
    test0_maze = parse_input(test0)
    test1_maze = parse_input(test1)
    maze = parse_input(puzzle)

    assert test0_pt1_ans == pt1(test0_maze)
    assert test1_pt1_ans == pt1(test1_maze)
    print(f"Part 1: {pt1(maze)}")

    assert test0_pt2_ans == pt2(test0_maze)
    assert test1_pt2_ans == pt2(test1_maze)
    print(f"Part 2: {pt2(maze)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

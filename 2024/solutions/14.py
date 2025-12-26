import os
import re
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
pt1_ans: int = 12
pt2_ans: int = 0


def parse_input(string: str):
    robots = {}  # {id: (px, py, vx, vy)}
    for i, line in enumerate(string.strip().splitlines()):
        # x-axis is columns, y-axis is rows
        px, py, vx, vy = map(int, re.findall(r'-?\d+', line))
        robots[i] = (px, py, vx, vy)

    return robots


def safety_score(robots, h, w):
    # given a map of robots and their locations, return the safety score

    # populate grid
    grid = [[0 for _ in range(w)] for _ in range(h)]
    for i, (px, py, _, _) in robots.items():
        assert 0 <= px < len(grid[0])
        assert 0 <= py < len(grid)
        grid[py][px] += 1

    # determine how many are in each quadrant
    q1 = sum(el for row in grid[:h // 2]
             for el in row[:w // 2])

    q2 = sum(el for row in grid[:h // 2]
             for el in row[1 + (w // 2):])

    q3 = sum(el for row in grid[1 + (h // 2):]
             for el in row[:len(grid[0]) // 2])

    q4 = sum(el for row in grid[1 + (h // 2):]
             for el in row[1 + (w // 2):])

    # calc score
    return q1 * q2 * q3 * q4


def pt1(robots, h, w):
    # move each robot to where it will be in 100 seconds
    # modulo operator takes care of overlapping
    robots = robots.copy()
    for i, (px, py, vx, vy) in robots.items():
        px = (px + 100 * vx) % w
        py = (py + 100 * vy) % h
        robots[i] = (px, py, vx, vy)

    # return safety score caluclation
    return safety_score(robots, h, w)


def pt2(robots, h, w):
    tree_iteration = None
    # at h*w seconds, the entire grid has reset due to the nature of the modulo operator
    for second in range(h * w):
        robots_ = robots.copy()
        for i, (px, py, vx, vy) in robots_.items():
            px = (px + second * vx) % w
            py = (py + second * vy) % h
            robots_[i] = (px, py, vx, vy)

        # populate grid for robot positions
        grid = [[0 for _ in range(w)] for _ in range(h)]
        for i, (px, py, _, _) in robots_.items():
            assert 0 <= px < len(grid[0])
            assert 0 <= py < len(grid)
            grid[py][px] += 1

        # ASSUMPTION, in the tree drawing all robots will be in different locations
        if len(robots) == len([ch for i, row in enumerate(grid) for j, ch in enumerate(row) if ch != 0]):
            tree_iteration = second
            print('\n'.join((''.join(map(str, row)) for row in grid)))
    return tree_iteration


def main(puzzle: str):
    test_robots = parse_input(test)
    robots = parse_input(puzzle)

    assert pt1_ans == pt1(test_robots, 7, 11)
    print(f"Part 1: {pt1(robots, 103, 101)}")

    print(f"Part 2: {pt2(robots, 103, 101)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

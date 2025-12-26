import os
from copy import deepcopy
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test0: str = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""

test1: str = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
pt1_ans: int = 10092
pt2_ans: int = 9021


def parse_input(string: str):
    grid, char_moves = string.split('\n\n')
    grid = [list(line) for line in grid.splitlines()]
    char_moves = ''.join([line for line in char_moves.splitlines()])
    moves = []
    for ch in char_moves:
        if ch == '<':
            moves.append((0, -1))
        elif ch == '>':
            moves.append((0, 1))
        elif ch == '^':
            moves.append((-1, 0))
        elif ch == 'v':
            moves.append((1, 0))

    return grid, moves


def pt1(grid, moves):
    def move(r, c, dr, dc, grid):
        """
        Perform move for robot in front of box
        """
        p, q = r+dr, c+dc

        # we find the next non-box spot (p, q)
        while grid[p][q] == 'O':
            p += dr
            q += dc

        char = grid[p][q]

        # reached a wall, can't move anything
        if char == '#':
            return grid, (r, c)
        # found empty spot, iteratively move all previous boxes and robot forwards
        elif char == '.':
            # move everything from the robot onwards one over by switching adjacent spots
            while (p, q) != (r, c):
                grid[p][q], grid[p-dr][q-dc] = grid[p-dr][q-dc], grid[p][q]
                p -= dr
                q -= dc
            return grid, (r + dr, c + dc)
        else:
            raise Exception(
                'This case should not have been reached, something is wrong')

    # initial position
    pos, = [(i, j) for i, row in enumerate(grid)
            for j, ch in enumerate(row) if ch == '@']

    """
    Moving rules:
    As the robot (@) attempts to move, if there are any boxes (O) in the way,
    the robot will also attempt to push those boxes. However, if this action
    would cause the robot or a box to move into a wall (#), nothing moves
    instead, including the robot. The initial positions of these are shown on
    the map at the top of the document the lanternfish gave you.
    """
    for (dr, dc) in moves:
        r, c = pos  # coordinates

        # next piece is a wall, so robot is not moving
        if grid[r+dr][c+dc] == '#':
            pos = (r, c)
        # next piece is empty spot, so switch empty spot and robot
        elif grid[r+dr][c+dc] == '.':
            grid[r+dr][c+dc], grid[r][c] = grid[r][c], grid[r+dr][c+dc]
            pos = (r + dr, c + dc)  # robot moves one space
        # next spot is a box, so we check if there is an empty space in front of it somewhere and move it
        elif grid[r+dr][c+dc] == 'O':
            grid, pos = move(r, c, dr, dc, grid)
        # print('\n'.join([''.join(line) for line in grid]))

    # return sum of gps coordinates of boxes
    return sum(100*i + j for i, row in enumerate(grid) for j, ch in enumerate(row) if ch == 'O')


def pt2(grid, moves):
    def resize_grid():
        new_grid = [[] for row in grid]
        for i, row in enumerate(grid):
            for ch in row:
                if ch == '#':
                    new_grid[i].extend(['#', '#'])
                elif ch == 'O':
                    new_grid[i].extend(['[', ']'])
                elif ch == '.':
                    new_grid[i].extend(['.', '.'])
                elif ch == '@':
                    new_grid[i].extend(['@', '.'])
        return new_grid

    grid = resize_grid()

    # initial position
    pos, = [(i, j) for i, row in enumerate(grid)
            for j, ch in enumerate(row) if ch == '@']

    for dr, dc in moves:
        # array of positions of objects that will be impacted by robot moving, first and foremost the robot itself!
        targets = [pos]
        go = True  # dirty bit will only be turned off if we encounter a wall somewhere
        # iterate over all targets, we change the list during iteration, so this will exhaustively check for boxes and walls
        for cr, cc in targets:
            nr, nc = cr + dr, cc + dc
            if (nr, nc) in targets:  # if we're adding a target twice, no need
                continue
            obj = grid[nr][nc]
            # its a wall, can't go anywhere, boohoo
            if obj == '#':
                go = False
                break
            # running into the left portion of a box
            if obj == '[':
                # append left and right portions of the box
                targets.append((nr, nc))
                targets.append((nr, nc + 1))
            # running into the right portion of a box
            if obj == ']':
                targets.append((nr, nc))
                targets.append((nr, nc - 1))
        if not go:
            continue
        # shallow copy to keep track of previous positions and characters
        copy_grid = list(list(row) for row in grid)

        # move the robot out of the current space!
        r, c = pos
        grid[r][c] = '.'
        grid[r+dr][c+dc] = '@'

        # move all boxes out of their current spaces
        for br, bc in targets[1:]:
            grid[br][bc] = '.'

        # move all boxes into their new spaces
        for br, bc in targets[1:]:
            grid[br+dr][bc+dc] = copy_grid[br][bc]

        pos = (r + dr, c + dc)
    # return sum of gps coordinates of boxes
    # print('\n'.join([''.join(line) for line in grid]))

    return sum(100*i + j for i, row in enumerate(grid) for j, ch in enumerate(row) if ch == '[')


def main(puzzle: str):
    test_grid, test_moves = parse_input(test1)
    grid, moves = parse_input(puzzle)

    assert pt1_ans == pt1(test_grid, test_moves)
    print(f"Part 1: {pt1(grid, moves)}")

    test_grid, test_moves = parse_input(test1)
    grid, moves = parse_input(puzzle)

    assert pt2_ans == pt2(test_grid, test_moves)
    print(f"Part 2: {pt2(grid, moves)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

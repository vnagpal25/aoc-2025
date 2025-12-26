import os
import re
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
pt1_ans: int = 480


def parse_input(string: str):
    blocks = string.strip().split("\n\n")
    ret = []

    for block in blocks:
        nums = list(map(int, re.findall(r"\d+", block)))
        ret.append(nums)

    return ret


def pt1(block_nums):
    """
    Brute forcing solution
    """
    total = 0
    for nums in block_nums:
        ax, ay, bx, by, px, py = nums
        min_score = float('inf')

        # max amount of presses is 100 total on each button
        for i in range(101):
            for j in range(101):
                if ax * i + bx * j == px and ay * i + by * j == py:
                    min_score = min(min_score, i*3 + j)
                    ...

        if min_score != float('inf'):
            total += min_score

    return total


def pt2(block_nums):
    """
    System of linear equations solution
    """
    total = 0
    for nums in block_nums:
        ax, ay, bx, by, px, py = nums

        # add 10000000000000 to px and py
        px += 10000000000000
        py += 10000000000000

        """
        System of equations:
        
        s is number of times that we press the A button
        t is number of times that we press the B button
        
        a_x * s + b_x * t = p_x
        a_y * s + b_y * t = p_y
        
        only has a unique solution when the determinant of the coefficient matrix:
        else, there is an infinite number of solutions
        a_x * b_y - a_y * b_x is non zero
        """
        determinant = ax * by - ay * bx
        if determinant != 0:
            s = (px * by - py * bx) / determinant
            t = (py * ax - px * ay) / determinant

            if int(s) == s and int(t) == t:
                total += int((s * 3 + t))
    return total


def main(puzzle: str):
    test_block = parse_input(test)
    block = parse_input(puzzle)

    assert pt1_ans == pt1(test_block)
    print(f"Part 1: {pt1(block)}")

    print(f"Part 2: {pt2(block)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

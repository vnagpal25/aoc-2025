import os
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
pt1_ans: int = 3749
pt2_ans: int = 11387


def parse_input(string: str):
    parsed = {int(line.split(':')[0]): list(map(int, line.split(':')[1].split()))
              for line in string.splitlines()}
    return parsed


# recursive solution
def possible_recur(sol, operands):
    if len(operands) == 1:
        return sol == operands[0]
    el = operands[-1]
    if sol % el == 0 and possible_recur(sol / el, operands[:-1]):
        return True
    elif sol - el >= 0 and possible_recur(sol - el, operands[:-1]):
        return True
    return False

# iterative solution


def possible(sol, operands):
    values = {operands[0]}
    for operand in operands[1:]:
        new_values = set()
        for value in values:
            # only add if the final solution is at least value + operand
            if sol >= value + operand:
                new_values.add(value + operand)
            # only multipy if the final solution is a multiple of the value
            # if sol % operand == 0:
            new_values.add(value * operand)
        values = new_values
    return sol in values


def possible_pt2(sol, operands):
    if len(operands) == 1:
        return sol == operands[0]
    el = operands[-1]
    if sol % el == 0 and possible_pt2(sol // el, operands[:-1]):
        return True
    if sol > el and possible_pt2(sol - el, operands[:-1]):
        return True
    str_sol = str(sol)
    str_el = str(el)
    if len(str_sol) > len(str_el) and str_sol.endswith(str_el) and possible_pt2(int(str_sol[:-len(str_el)]), operands[:-1]):
        return True
    return False


def pt1(equations):
    total = 0
    for value, operands in equations.items():
        # if possible(value, operands):
        if possible_recur(value, operands):
            total += value
    return total


def pt2(equations):
    total = 0
    for value, operands in equations.items():
        if possible_pt2(value, operands):
            total += value
    return total


def main(puzzle: str):
    test_input = parse_input(test)
    puzzle_input = parse_input(puzzle)

    assert pt1_ans == pt1(test_input)
    print(f"Part 1: {pt1(puzzle_input)}")

    assert pt2_ans == pt2(test_input)
    print(f"Part 2: {pt2(puzzle_input)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

import re

day: str = "03"

test1: str = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
test2: str = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
pt1_ans: int = 161
pt2_ans: int = 48


def pt1(puzzle):
    # matches will return a list of tuple values (x, y) such that mul(x, y) was in the pattern
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    instructions = re.findall(pattern, puzzle)
    return sum(int(num1) * int(num2) for num1, num2 in instructions)


def pt2(puzzle):
    delims = ["don't()", 'do()']

    # Escape special regex characters like parentheses
    # combine split patterns as a regex that matches any of the delimeters
    split_pattern = '|'.join([re.escape(d) for d in delims])

    # Split the string into parts and delimiters
    parts_and_delims = re.split(f'({split_pattern})', puzzle)

    # extract parts that follow do() and the first part before don't()
    do_str = f'{parts_and_delims[0]}'
    for i in range(0, len(parts_and_delims), 2):
        # First part always has an empty preceding delimiter
        preceding_delim = parts_and_delims[i-1] if i > 0 else ''
        part = parts_and_delims[i]

        if part and preceding_delim == 'do()':  # Only add non-empty parts
            do_str += part

    # run the part 1 regex matching on resulting string
    return pt1(do_str)


def main(puzzle: str):
    assert pt1_ans == pt1(test1)
    print(f"Part 1: {pt1(puzzle)}")

    assert pt2_ans == pt2(test2)
    print(f"Part 2: {pt2(puzzle)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

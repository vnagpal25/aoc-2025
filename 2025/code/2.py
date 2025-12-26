import os

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def num_digits(): ...


def part1(puzzle: str):
    ranges = []
    for interval in puzzle.split(","):
        s, e = interval.split("-")
        if len(s) < len(e):
            # we need to clip the range
            if len(s) % 2:
                # s is an odd length number
                s = "1" + "0" * (len(e) - 1)
            else:
                # e is an odd length number
                e = "9" * len(s)

        # if odd digit length range
        if len(s) % 2:
            continue

        ranges.append((int(s), int(e), len(s)))

    to_ret = 0
    for s, e, length in ranges:
        number = int("1" + ("0" * (length // 2 - 1)) + "1")

        # how many are multiples from 1 to s
        # minus how many are multiples 1 to e
        num_multiples = e // number - s // number
        if not s % number:
            num_multiples += 1

        if not num_multiples:
            continue

        # find first multiple
        first = s
        if s % number:
            first = number * ((s // number) + 1)

        # print(num_multiples)
        # print(s, e)
        for invalid in range(num_multiples):
            # print(first + (number * invalid))
            to_ret += first + (number * invalid)

    return to_ret


def part2(puzzle: str):
    ranges = [list(map(int, interval.split("-"))) for interval in puzzle.split(",")]
    numbers = sum((list(range(start, end + 1)) for start, end in ranges), [])
    total = 0
    for number in numbers:
        string = str(number)
        # need to check if some sequence repeats
        for seq_len in range(1, 1 + len(string) // 2):
            if len(string) % seq_len:
                continue
            multiple = len(string) // seq_len
            if string[:seq_len] *multiple == string:
                total+=number
                break
    return total

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

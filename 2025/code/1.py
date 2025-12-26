import os

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    puzzle = puzzle.splitlines()

    dial = 50

    password = 0
    for inst in puzzle:
        if "R" in inst:
            shift = int(inst.strip("R"))
        else:
            shift = -1 * int(inst.strip("L"))

        dial = (shift + dial) % 100

        if dial == 0:
            password += 1

    return password


def part2(puzzle: str):
    puzzle = puzzle.splitlines()

    dial = 50

    password = 0
    for inst in puzzle:
        # print(f"Dial: {dial}")

        if "R" in inst:
            new = dial + int(inst[1:])
            passes = new // 100
            # print(f"Shift right by {int(inst.strip("R"))}, pass 0 {passes} times")
        else:
            s = dial
            dist = int(inst[1:])
            if s == 0:
                passes = (
                    dist // 100
                )  # we start at zero so we count how many times we will pass excluding the start
            elif s > dist:
                passes = 0 # we don't go past 0
            else:
                # dist >= s, so we pass 0 at least once (+ 1
                # the rest of the passes the remaining dist // 100
                passes = 1 + (dist - s) // 100 # s is not zero, so we add an extra pass

            new = s - dist

        password += passes
        dial = new % 100

    return password


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

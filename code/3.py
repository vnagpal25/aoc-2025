import os

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    banks = [list(map(int, list(bank))) for bank in puzzle.splitlines()]
    total = 0
    for bank in banks:
        ones = bank[-1]
        tens = bank[-2]

        # whenever we find a bigger 10s spot, we bump up the ones to the old tens spot (if its larger)
        for i in range(len(bank) - 3, -1, -1):
            # can shift tens digit
            if bank[i] >= tens:

                # we also shift ones digit is the current tens spot is larger
                if tens >= ones:
                    ones = tens
                # shift tens spot over
                tens = bank[i]

        total += tens * 10 + ones
    return total


def part2(puzzle: str):
    banks = [list(map(int, list(bank))) for bank in puzzle.splitlines()]
    total = 0
    for bank in banks:
        number = bank[-12:]
        for i in range(len(bank) - 13, -1, -1):
            
            # same strategy as part1
            # this time we do the shift in a loop
            replacement = bank[i]
            to_replace = 0

            # while the new number is larger than the largest tens place
            shift = True
            while shift and to_replace < 12 and replacement >= number[to_replace]:
                # if we have numbers to shift over and the number we're replacing is larger than the next number
                if to_replace < 11 and number[to_replace] >= number[to_replace + 1]:
                    # move it over
                    new_replacement = number[to_replace + 1]
                    number[to_replace + 1] = number[to_replace]
                else:
                    # no need to keep shifting
                    shift = False
                # replace largest number
                number[to_replace] = replacement

                # +=2 because we already handled 2 digit placesa
                replacement = new_replacement
                to_replace += 2

        total += int("".join(map(str, number)))
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

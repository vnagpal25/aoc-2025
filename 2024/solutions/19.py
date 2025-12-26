import os
from typing import Set, List
from functools import cache
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
pt1_ans: int = 6
pt2_ans: int = 16


def parse_input(string: str):
    components, patterns = string.strip().split('\n\n')
    components = set(components.split(', '))
    patterns = patterns.split('\n')
    return components, patterns


def pt1(components: Set[str], patterns: List[str]):
    @cache
    def constructible(pattern: str):
        """
        Checks if a pattern is constructible with a given set of components.
        We loop over all components and if the pattern starts with a component,
        we chop it off the pattern and see if the resulting smaller string can be
        constructed recursively. Empty string is base case.

        We cache the results of this function to avoid repeated computations.
        """
        if not pattern:
            return True
        for comp in components:
            if pattern.startswith(comp) and constructible(pattern[len(comp):]):
                return True
        return False
    return len([pattern for pattern in patterns if constructible(pattern)])


def pt2(components: Set[str], patterns: List[str]):
    @cache
    def num_constructions(pattern):
        """
        Checks the number of ways that a pattern is constructible with a given set of components.
        We loop over all components and if the pattern starts with a component,
        we chop it off the pattern and see if the resulting smaller string can be
        constructed recursively. Empty string is base case, which means that the 
        string can be constructed so we return 1. Else we keep track of a 
        count variable and increment it with the number of ways that resulting 
        substrings can be formed.

        We cache the results of this function to avoid repeated computations.
        """
        if not pattern:
            return 1
        count = 0
        for comp in components:
            if pattern.startswith(comp):
                count += num_constructions(pattern[len(comp):])
        return count
    return sum(num_constructions(pattern) for pattern in patterns)


def main(puzzle: str):
    test_comps, test_patterns = parse_input(test)
    components, patterns = parse_input(puzzle)

    assert pt1_ans == pt1(test_comps, test_patterns)
    print(f"Part 1: {pt1(components, patterns)}")

    assert pt2_ans == pt2(test_comps, test_patterns)
    print(f"Part 2: {pt2(components, patterns)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

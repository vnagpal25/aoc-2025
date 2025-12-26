from collections import defaultdict
from functools import cmp_to_key
from typing import List

day: str = "05"

test: str = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
pt1_ans: int = 143
pt2_ans: int = 123


def parse_input(string: str):
    rules_txt, updates_text = string.split('\n\n')

    # parse update rules
    rules: defaultdict[set] = defaultdict(set)
    rules_txt = [rule.split('|') for rule in rules_txt.splitlines()]
    for p1, p2 in rules_txt:
        rules[p1].add(p2)

    # parse updates
    updates = [update.split(',') for update in updates_text.splitlines()]

    return rules, updates


def pt1(rules, updates):
    total = 0  # to return
    incorrect_updates: List[List[str]] = []

    # iterate over all updates
    for update in updates:
        # for each page in the update, check if the following pages are a subset of the allowed pages as defined by the rules
        for i, num in enumerate(update):
            if not set(update[i+1:]).issubset(rules[num]):
                incorrect_updates.append(update)
                break
        else:
            # loop exited normally, add the middle element to the total
            total += int(update[len(update) // 2])
    return total, incorrect_updates


def pt2(rules: defaultdict, incorrect_updates: List[List[str]]):
    # convert rules to a map of tuple (a,b) to either 1 or -1, -1 if in correct order 1 if not in correct order
    new_rules = {}
    for p1, p2s in rules.items():
        for p2 in p2s:
            new_rules[(p1, p2)] = -1
            new_rules[(p2, p1)] = 1

    # comparator function returns -1 or 1 depending on if they are incorrectly or correctly ordered
    def cmp(x, y):
        return new_rules[(x, y)]

    total = 0
    for update in incorrect_updates:
        # sort the update using built-in sort by providing it the comparator key 
        update.sort(key=cmp_to_key(cmp))
        # add middle number to total
        total += int(update[len(update) // 2])
    return total


def main(puzzle: str):
    test_rules, test_updates = parse_input(test)
    rules, updates = parse_input(puzzle)

    test_ans, test_incorrect = pt1(test_rules, test_updates)
    assert pt1_ans == test_ans
    ans, incorrect_updates = pt1(rules, updates)
    print(f"Part 1: {ans}")

    assert pt2_ans == pt2(test_rules, test_incorrect)
    print(f"Part 2: {pt2(rules, incorrect_updates)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

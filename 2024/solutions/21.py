import os
from collections import deque
from itertools import product
from functools import cache
from tqdm import tqdm
from typing import List
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """029A
980A
179A
456A
379A
"""
pt1_ans: int = 126384


numerical_keypad = (('7', '8', '9'),
                    ('4', '5', '6'),
                    ('1', '2', '3'),
                    (None, '0', 'A'))

directional_keypad = ((None, '^', 'A'),
                      ('<', 'v', '>'))


def parse_input(string: str):
    return string.strip().splitlines()


def find_sequences(keypad):
    """Precompute and return a map of the form:
    {(x, y): []}, where x and y are keys on the keypad and the associated list
    contains all possible button sequences with the least amount of button presses
    """
    # get the position of each element in the keypad
    pos = {el: (i, j) for i, row in enumerate(keypad)
           for j, el in enumerate(row) if el}

    # to return
    button_sequences = {}

    def bfs(x, y) -> List[str]:
        """
        Do a breadth first search over the keypad starting at position x
        Return all possible optimal moves from x to y
        """
        possibilites = []
        # keeps track of the position and the moves needed to get to that position
        q = deque([(pos[x], "")])
        # keeps track of optimal cost to reach y
        best = float("inf")
        while q:
            # get position and made moves
            (r, c), moves = q.popleft()

            # explore in all 4 directions
            for dr, dc, move in [(-1, 0, '^'), (1, 0, 'v'), (0, 1, '>'), (0, -1, '<')]:
                nr, nc = r + dr, c + dc

                # out of bounds
                if not 0 <= nr < len(keypad) or not 0 <= nc < len(keypad[0]):
                    continue

                # none tile
                if keypad[nr][nc] is None:
                    continue

                # reached goal
                if keypad[nr][nc] == y:
                    # we won't find any other cheaper paths after this
                    # due to nature of BFS, so we return
                    if best < len(moves) + 1:
                        return possibilites

                    # found an optimal sequence of moves, we end it with pressing A and append to possibilities
                    best = len(moves) + 1
                    possibilites.append(moves + move + 'A')
                else:
                    # keep exploring
                    q.append(((nr, nc), moves + move))
        # the only way to not reach this portion of code is if the two tiles are adjacent, so we return
        return possibilites

    # get all n^2 pairs of keys on the keypad
    for x in pos:
        for y in pos:
            # two keys are identical, so we're already where we need to be, so we just press A
            if x == y:
                button_sequences[(x, y)] = ['A']
                continue
            # else, we do a bfs to determine the optimal sequences
            button_sequences[(x, y)] = bfs(x, y)

    return button_sequences


def pt1(patterns, numpad_seqs, dirpad_seqs):
    total = 0

    def solve(string, seqs):
        """Return all optimal move strings that accomplish the code"""
        # x and y are adjacent characters in the string A + code
        # we prepend A because keypad starts at A
        # example string 029A
        # We go from A->0->2->9->A,
        # so we need to find all possible sequences of moves for those 4 transitions
        options = [seqs[(x, y)]
                   for x, y in zip('A' + string, string)]
        # product(*options) takes cartesian product of all possible sequences for each transition
        # this is a list of moves that would take us from A to A (A->0->2->9->A)
        all_possible_moves = product(*options)

        # we join all of the moves to return an array of strings
        return ["".join(moves) for moves in all_possible_moves]

    for code in patterns:
        # we get all possible numeric keypad sequence
        next = solve(code, numpad_seqs)

        # we solve the 2 directional keypad strings
        for _ in range(2):
            possible_next = []
            for move_string in next:
                possible_next += solve(move_string, dirpad_seqs)
            # calculates the length of the shortest move string and filters
            optimal_next = min(map(len, possible_next))
            next = [
                moves for moves in possible_next if len(moves) == optimal_next]

        # calculates score
        total += len(next[0]) * int(code[:-1])

    return total


def pt2(patterns, numpad_seqs, dirpad_seqs, depth):
    # get the length of the shortest sequence between each key on the number pad
    dir_lens = {pair: len(val[0]) for pair, val in dirpad_seqs.items()}

    # Instead of calculating the strings passed to each robot in a BFS type fashion, which would exponentially blow up in input size
    # We instead calculate the length of the string passed to each robot at a particular depth in a recursive fashion,
    # caching our results to avoid repeated computation
    @cache
    def compute_length(move_string, depth):
        """
        Computes the length of the end string that the last robot types 
        given a string typed a particular depth n(nth robot)
        """

        # first robot, we simply take the sum of the shortest sequence between each character in the string
        if depth == 1:
            return sum(dir_lens[(x, y)] for x, y in zip('A' + move_string, move_string))

        # else for each adjacent pair x,y in (A + string)
        # we take all of the string between x and y
        # then we compute the length of those strings typed at depth n-1
        # and take the minimum end length
        # we sum all of these minimum end lengths and return them
        total = 0
        for x, y in zip('A' + move_string, move_string):
            total += min(compute_length(string, depth-1)
                         for string in dirpad_seqs[(x, y)])
        return total

    def solve(string, seqs):
        """Return all optimal move strings that accomplish the code"""
        # x and y are adjacent characters in the string A + code
        # we prepend A because keypad starts at A
        # example string 029A
        # We go from A->0->2->9->A,
        # so we need to find all possible sequences of moves for those 4 transitions
        options = [seqs[(x, y)]
                   for x, y in zip('A' + string, string)]
        # product(*options) takes cartesian product of all possible sequences for each transition
        # this is a list of moves that would take us from A to A (A->0->2->9->A)
        all_possible_moves = product(*options)

        # we join all of the moves to return an array of strings
        return ["".join(moves) for moves in all_possible_moves]

    total = 0
    for code in patterns:
        # similar to pt1, we get all possible numeric keypad sequence for the specific string
        robot1 = solve(code, numpad_seqs)

        # calculates complexity in a recursive fashion
        total += min(compute_length(move_string, depth)
                     for move_string in robot1) * int(code[:-1])

    stats = compute_length.cache_info()
    print(f"Cache hits: {stats.hits}, Cache misses: {stats.misses}")

    return total


def main(puzzle: str):
    test_patterns = parse_input(test)
    patterns = parse_input(puzzle)

    numpad_seqs = find_sequences(numerical_keypad)
    dirpad_seqs = find_sequences(directional_keypad)

    assert pt1_ans == pt1(test_patterns, numpad_seqs, dirpad_seqs)
    print(f"Part 1 (Not optimized): {pt1(patterns, numpad_seqs, dirpad_seqs)}")
    print(
        f"Part 1 (Optimized): {pt2(patterns, numpad_seqs, dirpad_seqs, depth=2)}")

    print(
        f"Part 2 (Optimized): {pt2(patterns, numpad_seqs, dirpad_seqs, depth=25)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

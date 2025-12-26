import os
from collections import deque
from functools import cache
import pulp
import numpy as np

day = os.path.basename(__file__).split(".")[0]

SAMPLE = True
PUZZLE = True


def part1(puzzle: str):
    total = 0
    for machine in puzzle.splitlines():
        indicator, *buttons, _ = machine.split()

        # cast as binary integer
        goal = "".join(["1" if x == "#" else "0" for x in list(indicator[1:-1])])
        state_len = len(goal)
        goal = int(goal, 2)

        # cast all button indices to ints
        buttons = [list(map(int, button[1:-1].split(","))) for button in buttons]

        buttons_binary = []
        for button in buttons:
            state = ["0"] * state_len
            for index in button:
                state[index] = "1"
            buttons_binary.append(int("".join(state), 2))

        # graph search problem with 2^n nodes
        # BFS gaurantees the shortest path to any state
        # when the edges are of uniform weight

        # start with all switches off and 0 presses
        seen = {0}
        q = deque([(0, 0)])

        while q:
            state, presses = q.popleft()
            # if goal state reached, we take the number of presses and add to total sum
            if state == goal:
                total += presses
                break

            for button in buttons_binary:
                new_state = state ^ button
                if new_state in seen:
                    continue
                q.append((new_state, presses + 1))
                seen.add(new_state)

    return total


def part2(puzzle: str):
    total = 0
    for machine in puzzle.splitlines():
        _, *buttons, joltage = machine.split()

        b = np.array(list(map(int, joltage[1:-1].split(","))))

        # cast all button indices to ints
        A = np.zeros((len(b), len(buttons)))
        for j, button in enumerate(buttons):
            indices = list(map(int, button[1:-1].split(",")))
            for i in indices:
                A[i][j] = 1

        # Create problem
        prob = pulp.LpProblem("Minimize_Sum", pulp.LpMinimize)

        # Create variables (non-negative integers)
        x = [
            pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer")
            for i in range(A.shape[1])
        ]

        # Objective: minimize sum(n_i)
        prob += pulp.lpSum(x)

        # Constraints: Ax = b
        for i in range(len(b)):
            prob += pulp.lpSum(A[i][k] * x[k] for k in range(len(x))) == b[i]

        # Solve
        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        # Extract solution
        x_solution = [v.varValue for v in x]
        # print(f"Solution: {x_solution}")
        num_presses = sum(x_solution)
        total += num_presses
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

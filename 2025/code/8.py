import os
import numpy as np
import math

day = os.path.basename(__file__).split(".")[0]

SAMPLE = False
PUZZLE = True


def part1(puzzle: str):
    coords = np.array(
        [list(map(int, vector.split(","))) for vector in puzzle.splitlines()]
    )
    # pairwise displacement
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    # pairwise distance ()
    distances = np.sqrt(np.sum(diff**2, axis=-1))

    # get upper triangular indices (excluding main diagonal so k = 1)
    i_upper, j_upper = np.triu_indices_from(distances, k=1)

    # get the distances from upper triangle
    upper_distances = distances[i_upper, j_upper]

    # find indices of n smallest distances
    if SAMPLE:
        n = 10
    if PUZZLE:
        n = 1000
    smallest_idx = np.argpartition(upper_distances, n - 1)[:n]
    smallest_idx = smallest_idx[np.argsort(upper_distances[smallest_idx])]

    # contains the (i, j) indices of the n closest pairs
    pairs = [(int(i_upper[idx]), int(j_upper[idx])) for idx in smallest_idx]

    circuits = [[] for i in range(len(coords))]
    for i, j in pairs:
        circuits[i].append(j)
        circuits[j].append(i)

    # dfs to count community size

    visited = set()
    community_sizes = []

    def dfs(node):
        visited.add(node)
        size = 1  # Count current node

        for neighbor in circuits[node]:
            if neighbor in visited:
                continue
            size += dfs(neighbor)

        return size

    # Run DFS from each unvisited node
    for node in range(len(coords)):
        if node not in visited:
            community_size = dfs(node)
            community_sizes.append(community_size)

    community_sizes.sort(reverse=True)
    return math.prod(community_sizes[:3])


def part2(puzzle: str):
    coords = np.array(
        [list(map(int, vector.split(","))) for vector in puzzle.splitlines()]
    )
    # pairwise displacement
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    # pairwise distance ()
    distances = np.sqrt(np.sum(diff**2, axis=-1))

    # get upper triangular indices (excluding main diagonal so k = 1)
    i_upper, j_upper = np.triu_indices_from(distances, k=1)

    # get the distances from upper triangle
    upper_distances = distances[i_upper, j_upper]

    # indices of smallest indices
    smallest_idx = np.argsort(upper_distances)

    # contains the (i, j) indices of the n closest pairs
    pairs = [(int(i_upper[idx]), int(j_upper[idx])) for idx in smallest_idx]

    # circuits = [[] for i in range(len(coords))]
    unconnected = set(range(len(coords)))

    # fully connect the graph
    for i, j in pairs:
        # print(f'Connecting: {coords[i], coords[j]}')
        if i in unconnected:
            unconnected.remove(i)
        if j in unconnected:
            unconnected.remove(j)

        if not unconnected:
            (x1, _, _), (x2, _, _) = coords[i], coords[j]
            return x1 * x2


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

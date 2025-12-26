import os
import pdb
from tqdm import tqdm
from collections import deque
from functools import cache
from networkx import Graph, draw
from itertools import combinations
import matplotlib.pyplot as plt

day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""
pt1_ans: int = 7
pt2_ans: str = 'co,de,ka,ta'


def parse_input(string: str):
    G = Graph()
    for line in string.strip().splitlines():
        G.add_edge(*line.split('-'))
    return G


def pt1(G: Graph):
    # print(G.neighbors())
    # draw(G, with_labels=True)
    # plt.show()

    # a three cluster is a set of 3 nodes that is interconnected
    # we use a set to avoid counting duplicates
    three_clusters = set()
    for x in G.nodes:
        # list all combinations of 2 neighbors of each node
        # and check if they are neighbors as well
        pairs = combinations(G.neighbors(x), 2)
        for y, z in pairs:
            if y in G.neighbors(z):
                # sorting avoids us adding duplicate clusters
                three_clusters.add(tuple(sorted((x, y, z))))

    # this will be a generator of booleans which are treated as 1 if true and 0 if false, so we return the sum of all Trues
    # equivalently number of all three clusters which have a computer that starts with t
    return sum(any(cn.startswith('t') for cn in cluster) for cluster in three_clusters)


def pt2(G):
    # keeps track of all interconnected sets of computers, deemed parties
    parties = set()

    def search(node, party):
        """
        Inputs:
        (1)set of interconnected computers(party) 
        (2)a computer (node) in (party)

        Does: checks all neighbors of node, and recursively expands party to include more interconnected nodes
        """

        # Checks if the current party has currently been explored
        # If so, we don't explore it again, as a larger party containing it has already been explored
        key = tuple(sorted(party))
        if key in parties:
            print('already searched')
            return

        # marks as explored
        parties.add(key)

        # checks all neighbors of node
        for neighbor in G.neighbors(node):
            # neighbor is already in party, so doesn't need to be explored
            if neighbor in party:
                continue

            # check if party is a subset of the neighbor's connections
            # essentially checks if the new neighbor is connected to every node in the party

            # both of the following are correct
            # if not all(neighbor in G.neighbors(party_member) for party_member in party):
            #     continue

            # if there is a node that is in the party but not connected, we continue
            if not set(party) <= set(G.neighbors(neighbor)):
                continue

            # we have found a new node not in party, but in node's neighbors that is also connected to the party
            # so we continue to expand this set
            search(neighbor, party | {neighbor})

    # find all parties containing each node 
    for node in G.nodes:
        search(node, {node})

    # get the largest set, sort it, and join by commas
    return ','.join(sorted(max(parties, key=len)))


def main(puzzle: str):
    Gt = parse_input(test)
    G = parse_input(puzzle)

    assert pt1_ans == pt1(Gt)
    print(f"Part 1: {pt1(G)}")

    assert pt2_ans == pt2(Gt)
    print(f"Part 2: {pt2(G)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

import sys
from collections import defaultdict
from itertools import cycle


def read_input():
  """
  Read input and return
  - a direction string
  - a dictionary representing the tree
  """
  with open(sys.argv[1], 'r') as file:
    sections = file.read().split("\n\n")
  directions, edges = sections  
  edges = edges.split('\n')
  tree = defaultdict(list)
  for edge in edges:
    node, neighbors = edge.split('=')
    node = node.strip()
    neighbors = neighbors.strip().strip('(').strip(')').split(',')
    neighbors = [neighbor.strip() for neighbor in neighbors]
    tree[node] = neighbors
  return directions, tree


def main():
  # read input
  directions, tree = read_input()

  # this maps indices within tree to left and right child
  direction_index_map = {'L': 0, 'R': 1}
  
  # starting node is 'AAA'
  # moves keeps track of total moves made
  curr = 'AAA'
  moves = 0

  # cycle allows for infinite repitition of direction string
  for direction in cycle(directions):
    # get left and right children for current node
    curr_neighbors = tree[curr]

    # get 0 or 1 depending on direction
    neighbor_index = direction_index_map[direction]

    # move to next node and update moves made
    curr = curr_neighbors[neighbor_index]
    moves += 1

    # Destination node reached, so break and print result
    if curr == 'ZZZ':
      print(f'Total moves required: {moves}')
      break


if __name__ == "__main__":
  main()

import sys
from collections import defaultdict
from itertools import cycle


def gcd(x, y):
  """
  Using Euclid's Algorithm to Compute the Greatest Common Divisor (GCD) of two numbers
  """
  x, y = max(x, y), min(x, y)
  if y == 0:
    return x
  return gcd(y, x % y)


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
  # read the input
  directions, tree = read_input()

  # this maps indices within tree to left and right child
  direction_index_map = {'L': 0, 'R': 1}

  # get the starting nodes
  starting_nodes = [node for node in tree.keys() if node.endswith('A')]

  # will contain the number of moves required for each path from a starting node **A to reach a destination node **Z
  cycle_lengths = []

  # iterate over all starting nodes
  for starting_node in starting_nodes:
    # keeps track of current node and moves taken
    curr = starting_node
    moves = 0

    # cycle causes the direction string to be repeated infinitely until we reach our destination node
    for direction in cycle(directions):
      # get left and right children of the current node
      curr_neighbors = tree[curr]
      
      # get 0 or 1 depending on the direction
      neighbor_index = direction_index_map[direction]
      
      # move to the next child and updates moves made
      curr = curr_neighbors[neighbor_index]
      moves += 1

      # reached a destination node so break out of infinite loop and append the result
      if curr.endswith('Z'):
        cycle_lengths.append(moves)
        break
  
  # lcm of the cycle lengths is the smallest number of moves required for all of paths from an A node to reach a Z node 
  # computing LCM(a, b) = (a * b)/gcd(a, b)
  lcm_cycle = 1
  for cycle_len in cycle_lengths:
    lcm_cycle  = (lcm_cycle * cycle_len)/gcd(lcm_cycle, cycle_len)

  print(f"Smallest total amount of moves required from each path(starting at **A) to ensure all paths are at a **Z node: {lcm_cycle}")


if __name__ == "__main__":
  main()

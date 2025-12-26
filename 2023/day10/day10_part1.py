import sys

sys.setrecursionlimit(10**5)

# Directions for each of the different connectors
directions = {
    '|': [(1, 0), (-1, 0)],
    '-': [(0, 1), (0, -1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)]
}


def accessible(node, node_loc, prev_loc):
   """
   Checks if a node is accessible from a previous location
   """
   row, col = node_loc # gets the node's coords

   # returns True if it is reachable from prev loc
   # False otherwise
   for row_d, col_d in directions[node]:
      if (row + row_d, col + col_d) == prev_loc:
         return True
   return False


def read_input():
  """
  Reads the input maze and returs the maze and size
  """
  with open(sys.argv[1], 'r') as file:
    maze = file.readlines()
  rows, cols = len(maze), len(maze[0])
  return maze, (rows, cols)


def dfs(maze, prev=None, start=None, visited=None, goal = 'S', path=None):
    """
    Performs Depth First Search to keep track of the path and find the goal node
    Once the goal node is found, we return the path to the node
    """
    row, col = start # extracts row and column

    # only perform dfs if it is a valid location
    if 0 <= row < len(maze) and 0 <= col <= len(maze[0]):
      # visited node
      if visited is None:
          visited = set()

      # create the path, append the current node to it
      if path is None:
         path = []
      path = path + [start]

      # extract the node, if the node is the S, return the path to it
      node = maze[row][col]
      if node == goal and len(path):
         return path

      # also checks if it is a connector node
      # checks if the node is accessible from the previous node, 
      # if so, performs DFS on its neighbors and adds it to visited
      if node in directions and accessible(node, start, prev):
        visited.add(start)

        # checks both directions of connector
        for row_d, col_d in directions[node]:
            
            # checks if not prev and not visited
            neighbor_loc = (row + row_d, col + col_d)
            if neighbor_loc not in visited and neighbor_loc != prev:
              new_path = dfs(maze, start, neighbor_loc, visited, path=path)
              if new_path:
                 return new_path
      return None


def find_start(maze):
   for i, row in enumerate(maze):
      for j, entry in enumerate(row):
         if entry == 'S':
            return (i, j)


def main():
  """
  | is a vertical pipe connecting north and south.
  - is a horizontal pipe connecting east and west.
  L is a 90-degree bend connecting north and east.
  J is a 90-degree bend connecting north and west.
  7 is a 90-degree bend connecting south and west.
  F is a 90-degree bend connecting south and east.
  . is ground; there is no pipe in this tile.
  S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
  """
  maze, size = read_input()
  start = find_start(maze)
  row, col = start

  for row_d, col_d in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
     start_row, start_col = row + row_d, col + col_d
     path = dfs(maze, prev=start, start=(start_row, start_col))
     if path:
        print(len(path) // 2)
        break

if __name__ == "__main__":
  main()

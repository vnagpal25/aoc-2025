from collections import deque
import sys


def read_input():
  """
  Reads the input maze and returs the maze and size
  """
  with open(sys.argv[1], 'r') as file:
    maze = file.readlines()
  rows, cols = len(maze), len(maze[0])
  return maze, (rows, cols)


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
  sr, sc = find_start(maze)
  seen = {(sr, sc)}
  q = deque([(sr, sc)])

  while q:
    r, c = q.popleft()
    ch = maze[r][c]

    # condition for going up
    # past the first row, current character allows us to go up, and next character allows us to go up as well
    # and the next character is unvisited
    if r > 0 and ch in "SL|J" and maze[r-1][c] in "|7F" and (r - 1, c) not in seen:
      seen.add((r-1, c))
      q.append((r-1, c))

    # condition for going down
    # before the last row,
    if r < len(maze) - 1 and ch in "S7F|" and maze[r+1][c] in "JL|" and (r + 1, c) not in seen:
      seen.add((r+1, c))
      q.append((r+1, c))

    # condition for going left
    if c > 0 and ch in "S7J-" and maze[r][c-1] in "-FL" and (r, c - 1) not in seen:
      seen.add((r, c-1))
      q.append((r, c-1))


    # condition for going right
    if c < len(maze[0]) - 1 and  ch in "SFL-" and maze[r][c+1] in "-J7" and (r, c + 1) not in seen:
      seen.add((r, c+1))
      q.append((r, c+1))
    
  print(len(seen) // 2)

if __name__ == "__main__":
  main()

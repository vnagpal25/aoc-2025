from collections import deque
import sys


def read_input():
  """
  Reads the input maze and returs the maze and size
  """
  with open(sys.argv[1], 'r') as file:
    maze = file.read().strip().splitlines()
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
  loop = {(sr, sc)}
  q = deque([(sr, sc)])
  maybe_s = {"|", "-", "F", "J", "L", "7"}
  while q:
    r, c = q.popleft()
    ch = maze[r][c]

    # condition for going up
    # past the first row, current character allows us to go up, and next character allows us to go up as well
    # and the next character is unvisited
    if r > 0 and ch in "SL|J" and maze[r-1][c] in "|7F" and (r - 1, c) not in loop:
      loop.add((r-1, c))
      q.append((r-1, c))
      if ch == "S":
        maybe_s &= {"L", "|", "J"}

    # condition for going down
    # before the last row,
    if r < len(maze) - 1 and ch in "S7F|" and maze[r+1][c] in "JL|" and (r + 1, c) not in loop:
      loop.add((r+1, c))
      q.append((r+1, c))
      if ch == "S":
        maybe_s &= {"7", "|", "F"}

    # condition for going left
    if c > 0 and ch in "S7J-" and maze[r][c-1] in "-FL" and (r, c - 1) not in loop:
      loop.add((r, c-1))
      q.append((r, c-1))
      if ch == "S":
        maybe_s &= {"-", "7", "J"}

    # condition for going right
    if c < len(maze[0]) - 1 and  ch in "SFL-" and maze[r][c+1] in "-J7" and (r, c + 1) not in loop:
      loop.add((r, c+1))
      q.append((r, c+1))
      if ch == "S":
        maybe_s &= {"L", "-", "F"}

  assert len(maybe_s) == 1
  (S, ) = maybe_s
  
  # replacing S with correct character
  maze = [row.replace("S", S) for row in maze]

  # replacing all characters within maze with "." that are not within the loop
  maze = ["".join(ch if (r, c) in loop else "." for c, ch in enumerate(row)) for r, row in enumerate(maze)]

  outside = set()

  for r, row in enumerate(maze):
    within = False # keeps track of whether we are within the loop or not
    up = None # keeps track of which direction the pipe is facing, initially none because we don't know
    # up also keeps track if we are 'riding' along a pipe
    # if up is not None, we hit  L or F pipe, and we are riding along some adjacent pipes
    # if up is None, we have been hitting vertical pipes or J7 pipes which means that
    # we haven't been riding along any pipes (rather crossing vertical ones or leaving horiztonal ones)
    
    for c, ch in enumerate(row):
      # horiztonal scanning, if we encounter a vertical pipe, we cross the loop
      # so we flip within (we either left or entered the loop)
      # up should be None here because we aren't traveling up or down when we hit a vertical pipe in a horizontal sweep
      if ch == "|":
        assert up is None
        within = not within
      
      # we encounter a horizontal pipe
      # which means that we have already hit a LF7J pipe
      # so up should have a value
      elif ch == "-": # riding along a pipe
        assert up is not None
      

      # we encounter a LF corner pipe
      # up should be none here because we shouldn't be riding along any pipes
      # when we hit these pipes
      # change the value of up
      # if its an L tube, then the maze is going "up"
      # else the maze is going down
      elif ch in "LF":
        assert up is None
        up = ch == 'L'
      
      # we encounter an 7J corner pipe
      # up should be non null here because we should have been riding along a pipe
      # if up is True, we hit an L pipe before
        # if the current pipe is a J, we're still riding along the pipe
        # if the current pipe is a 7, there is a direction switch and we cross
        # so we change the value of within
      # if up is False, we hit an F pipe before
        # if the current pipe is a 7, we're still riding along the pipe
        # if the current pipe is a J, there is a direction switchin and we cross
      elif ch in "7J":
        assert up is not None
        if ch != ("J" if up else "7"):
          within = not within
        up = None
      
      if not within:
        outside.add((r, c))

  print(f"{len(maze) * len(maze[0]) - len(outside | loop)} tiles within the loop")

  # Loop: all points that are in the loop
  # Outside: contains all points where we are not riding along a part of the maze or in the maze (effectively outside of the loop)
  # Outside | Loop: all points that are outside or on loop
  # not (Outside | Loop): all points that are enclosed the loop

  outside_on_loop = (outside | loop)
  for r in range(len(maze)):
    for c in range(len(maze[r])):
      # if its in outside - loop, it definitively outside the loop
      print("#" if (r, c) not in outside_on_loop else '.', end="")
    print()


if __name__ == "__main__":
  main()

import sys
from collections import deque


def run_beam(starting_config, grid):
  dir_map = {"/": -1, "\\": 1} # signs for reflcting mirrors
  
  # first two are starting coordinates, second two is the direction
  r, c, d_r, d_c = starting_config

  # switch direction of the beam based on mirror
  if grid[r][c] in ('\\', '/') and d_r == 0:
    d_r, d_c = dir_map[grid[r][c]], 0

  """
  Queue keeps track of the squares that we need to explore using the beam

  Dir squares keeps track of the squares/directions that have already been explored 
  """
  q = deque([(r, c, d_r, d_c)])
  dir_squares = {(r, c, d_r, d_c)}

  # if the starting character is a splitter, adjust queue/dir_squares accordingly
  if grid[r][c] == '|' and d_r == 0:
    q = deque([(r, c, 1, 0), (r, c, -1, 0)])
    dir_squares = {(r, c, 1, 0), (r, c, -1, 0)}
  if grid[r][c] == '-' and d_c == 0:
    q = deque([(r, c, 0, 1), (r, c, 0, -1)])
    dir_squares = {(r, c, 0, 1), (r, c, 0, -1)}

  # keeps track of explored squares
  seen_squares = {(r, c)}

  # while there are active beams to explore, keep exploring
  while q:
    # unpack popped element
    beam_row, beam_col, d_r, d_c = q.pop()

    # while the beam is inbounds
    while 0 <= beam_col + d_c < len(grid[0]) and 0 <= beam_row + d_r < len(grid):
      char = grid[beam_row + d_r][beam_col + d_c]

      # hits a reflector
      if char in ['/', '\\']:
        if d_r == 0: # horiontal beam
          (nd_r, nd_c) = (dir_map[char] * d_c, 0)
        else: # vertical beam
          (nd_r, nd_c) = (0, dir_map[char] * d_r)
        
        # only explore if not previously explored 
        if (beam_row + d_r, beam_col + d_c, nd_r, nd_c) not in dir_squares:
          q.appendleft((beam_row + d_r, beam_col + d_c, nd_r, nd_c))
          dir_squares.add((beam_row + d_r, beam_col + d_c, nd_r, nd_c))
        
          seen_squares.add((beam_row + d_r, beam_col + d_c))
        break
      
      # hits a horizontal splitter
      if char == '-' and d_c == 0:
        # sends it traveling left
        if (beam_row + d_r, beam_col + d_c, 0, -1) not in dir_squares:
          q.appendleft((beam_row + d_r, beam_col + d_c, 0, -1))
          dir_squares.add((beam_row + d_r, beam_col + d_c, 0, -1))
        
        # sends it traveling right
        if (beam_row + d_r, beam_col + d_c, 0, 1) not in dir_squares:
          q.appendleft((beam_row + d_r, beam_col + d_c, 0, 1))
          dir_squares.add((beam_row + d_r, beam_col + d_c, 0, 1))
        
        seen_squares.add((beam_row + d_r, beam_col + d_c))
        break
      
      # hits a vertical splitter
      if char == '|' and d_r == 0:
        # sends it traveling down
        if (beam_row + d_r, beam_col + d_c, 1, 0) not in dir_squares:
          q.appendleft((beam_row + d_r, beam_col + d_c, 1, 0))
          dir_squares.add((beam_row + d_r, beam_col + d_c, 1, 0))
        
        # sends it traveling up
        if (beam_row + d_r, beam_col + d_c, -1, 0) not in dir_squares:
          q.appendleft((beam_row + d_r, beam_col + d_c, -1, 0))
          dir_squares.add((beam_row + d_r, beam_col + d_c, -1, 0))

        seen_squares.add((beam_row + d_r, beam_col + d_c))
        break
      
      # if non signficant square, keep progressing in direction and add the square as seen
      beam_row, beam_col = beam_row + d_r, beam_col + d_c
      seen_squares.add((beam_row, beam_col))
  
  return seen_squares


def main():
  # Read input
  with open(sys.argv[1], 'r') as file:
    grid = file.read().strip().splitlines()
  
  # Part 1: run beam from starting point (0, 0) in direction (0, 1)
  seen_squares = run_beam((0, 0, 0, 1), grid)
  print(f'Answer to part 1: {len(seen_squares)}')

  # Part 2
  lengths = {len(seen_squares)} # holds the number of all possible lit up squares
   
  # run from left edge
  for (r, c) in ((x, 0) for x in range(1, len(grid))):
    lengths.add(len(run_beam((r, c, 0, 1), grid)))

  # run from right edge
  for (r, c) in ((x, len(grid)-1) for x in range(len(grid))):
    lengths.add(len(run_beam((r, c, 0, -1), grid)))
  
  # run from top edge
  for (r, c) in ((0, y) for y in range(len(grid[0]))):
    lengths.add(len(run_beam((r, c, 1, 0), grid)))
  
  # run from bottom edge
  for (r, c) in ((len(grid[0]) - 1, y) for y in range(len(grid[0]))):
    lengths.add(len(run_beam((r, c, -1, 0), grid)))
   
  print(f'Answer to part 2: {max(lengths)}')


if __name__ == "__main__":
  main()

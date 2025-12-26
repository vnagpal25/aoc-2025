import sys
import numpy as np

desired_iteration = 1000000000

# Cache for optimization

row_cache = {} # row: row
cycle_cache = {} # rocks: rocks 
directional_cache = {} # (rocks, dir): rocks


def tupify(rocks):
  return tuple([tuple(rock_row) for rock_row in rocks])


def read_input():
  with open(sys.argv[1], 'r') as file:
    return file.read().strip().splitlines()


def slide_row_west(rock_row):
  """
  Slides a row to the west
  """
  to_cache = tuple(rock_row)

  if to_cache not in row_cache:
    for j in range(len(rock_row)):
      
      curr = j
      while curr > 0 and rock_row[curr - 1] == '.' and rock_row[curr] == 'O':
        rock_row[curr - 1], rock_row[curr] = rock_row[curr], rock_row[curr - 1]
        curr -= 1
    row_cache[to_cache] = ''.join(rock_row)
  return row_cache[to_cache]  


def slide_west(rocks):
  """
  Slides a grid west
  """
  to_cache = tupify(rocks)

  if (to_cache, 'W') not in directional_cache:
    for i in range(len(rocks)):
      rocks[i] = slide_row_west(list(rocks[i]))

    directional_cache[(to_cache, 'W')] = rocks
  
  return directional_cache[(to_cache, 'W')]


def slide_north(rocks):
  """
  Slides a grid north
  """
  to_cache = tupify(rocks)
  if (to_cache, 'N') not in directional_cache:
    rocks = list(map(''.join, zip(*rocks)))
    
    rocks = slide_west(rocks)

    directional_cache[(to_cache, 'N')] = list(map(''.join, zip(*rocks)))

  return directional_cache[(to_cache, 'N')]


def slide_east(rocks):
  """
  Slides a grid east
  """
  to_cache = tupify(rocks)
  if (to_cache, 'E') not in directional_cache:
    for i in range(len(rocks)):
      rock_row = list(rocks[i])[::-1]
      rocks[i] = ''.join(slide_row_west(rock_row))[::-1]
    directional_cache[(to_cache, 'E')] = rocks
  return directional_cache[(to_cache, 'E')]


def slide_south(rocks):
  """
  Slides a grid south
  """
  to_cache = tupify(rocks)
  if (to_cache, 'S') not in directional_cache:
    rocks = np.array([list(rock_row) for rock_row in rocks])
    rocks = np.flip(rocks, axis=0)
    
    rocks = slide_north(list(rocks))
    rocks = np.array([list(rock_row) for rock_row in rocks])
    rocks = np.flip(rocks, axis=0)
    rocks = [''.join(rock_row) for rock_row in rocks]

    directional_cache[(to_cache, 'S')] = rocks
  return directional_cache[(to_cache, 'S')]


def main():
  # Read input
  rocks = read_input()

  # output answers
  total_part1 = total_part2 = 0
  
  # keeps track of the grid after each cycle
  cycle_cycle = []
  
  # part 1
  for i, rock_row in enumerate(slide_north(rocks)[::-1]):
    total_part1 += (i + 1) * rock_row.count('O')
  
  print(f'Answer to part 1: {total_part1}')


  # part 2, iterate until a cycle is detected then break
  for i in range(desired_iteration):
    tup_rocks = tupify(rocks)
    

    if tup_rocks not in cycle_cache:
      cycle_cycle.append(rocks)

      rocks = slide_north(rocks)

      rocks = slide_west(rocks)

      rocks = slide_south(rocks)

      rocks = slide_east(rocks)

      cycle_cache[tup_rocks] = rocks
    else:
      break
  
  # find the start of the cycle, the length of the cycle, and the index in the seen array where the desired state lies
  cycle_start = cycle_cycle.index(rocks)
  cycle_length = i - cycle_start
  desired_index = (desired_iteration - cycle_start) % cycle_length + cycle_start

  # gets the desired state
  rocks = cycle_cycle[desired_index]

  # answer for part 2
  for i, rock_row in enumerate(rocks[::-1]):
    total_part2 += (i + 1) * rock_row.count('O')
  
  print(f'Answer to part 2: {total_part2}')


if __name__ == "__main__":
  main()

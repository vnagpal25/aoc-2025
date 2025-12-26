import sys


def get_distances(universe, expansion_factor):
  """
  return an array of distances corresponding to the rows of the universe
  if there is an empty row increase distance by the expansion factor
  else increase by 1
  """
  distances = []
  curr_distance = 0
  for i, line in enumerate(universe):
    if line == "."*len(line):
      curr_distance += expansion_factor
    else:
      curr_distance += 1
    distances.append(curr_distance)
  return distances


def expand_universe(lines, expansion_factor):
  # get distance from start for each row
  d_rows = get_distances(lines, expansion_factor)

  # transpose and get distance for each column
  lines = [''.join(line) for line in zip(*lines)]
  d_cols = get_distances(lines, expansion_factor)

  # list comp. to make distance matrix
  distances = [[(d_r, d_c) for d_c in d_cols] for d_r in d_rows]
  return distances


def read_input():
  # read input
  with open(sys.argv[1], 'r') as file:
    lines = file.read().strip().splitlines()

  # get distance matrix (coordinates) for each point in the galaxy
  # using specific expansion factor
  distances_pt1 = expand_universe(lines, 2)
  distances_pt2 = expand_universe(lines, 1000000)

  return lines, distances_pt1, distances_pt2


def find_all_galaxies(universe):
  """
  Find coordinates of all of the galaxies
  """
  galaxy_coords = []  # [(i, j)]
  for i, row in enumerate(universe):
    for j, ch in enumerate(row):
      if ch == "#":
        galaxy_coords.append((i, j))

  return galaxy_coords


def main():
  # read input
  universe, distances_pt1, distances_pt2 = read_input()

  # get coords of all galaxies
  galaxy_coords = find_all_galaxies(universe)

  part_to_distance_map = {1: distances_pt1, 2: distances_pt2}

  for part, distances in part_to_distance_map.items():
    sum_ = 0
    for i in range(len(galaxy_coords)):
      i1, j1 = galaxy_coords[i] # get coords
      d1y, d1x = distances[i1][j1] # get distance coords

      for j in range(i+1, len(galaxy_coords)):
        i2, j2 = galaxy_coords[j] # get coords
        d2y, d2x = distances[i2][j2] # get distance coords

        # calculating minimum distance as d = |delta_x| + |delta_y|
        sum_ += (abs(d2x - d1x) + abs(d2y - d1y))

    print(f'Answer to part {part}: {sum_}')


if __name__ == '__main__':
  main()

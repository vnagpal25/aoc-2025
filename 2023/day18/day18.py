import sys


def mult(tup, c):
  # scalar multiplication
  return (c * tup[0], c * tup[1])


def plus(tup1, tup2):
  # vector addition
  return (tup1[0] + tup2[0], tup1[1] + tup2[1])


def main():
  # Reading input
  with open(sys.argv[1], 'r') as file:
    edges = file.read().strip().splitlines()

  # maps directions to vectors
  dir_map = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
  
  # maps numbers to directions(part 2)
  num_dir_map = {'0': 'R', '1':'D', '2':'L', '3':'U'}

  # hold corner points for the polygon 
  corners_pt1 = [(0, 0)]
  corners_pt2 = [(0, 0)]

  # stores the number of boundary points
  boundary_points_pt1 = boundary_points_pt2 = 0


  for edge in edges:
    # parsing input
    d, n, color = edge.split()
    n = int(n)
    color = color.strip('(').strip(')')

    # adding boundary points
    boundary_points_pt1 += n

    # adding next corner as last corner + n * (direction shift)
    corners_pt1.append(plus(mult(dir_map[d], n), 
                            corners_pt1[-1]))

    # part 2 parsing input
    n_2, d_2 = color[1:-1], color[-1]
    n_2 = int(n_2, 16)
    d_2 = num_dir_map[d_2]

    # adding boundary points
    boundary_points_pt2 += n_2

    # adding next corner
    corners_pt2.append(plus(mult(dir_map[d_2], n_2), 
                            corners_pt2[-1]))

  # finding area for each part
  for i, (corners, boundary_points) in enumerate([(corners_pt1, boundary_points_pt1), (corners_pt2, boundary_points_pt2)],1):
    # shoelace formula for polygon area
    area = abs(sum(corners[i][0] * (corners[i - 1][1] - corners[(i + 1) % len(corners)][1])for i in range(len(corners)))) // 2

    # pick's formula finds the area of interior polygon
    interior_points = area - (boundary_points // 2) + 1

    # adding interior and border
    final_area = interior_points + boundary_points

    # print answer
    print(f'Area for part {i}: {final_area}')


if __name__ == "__main__":
  main()

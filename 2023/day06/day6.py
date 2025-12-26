import sys
import cmath, math

def get_roots(time, distance):
  # quadratic formula calculation
  a = -1
  b = time
  c = -1 * distance 

  d = (b**2) - (4*a*c)  

  sol1 = ((-b-cmath.sqrt(d))/(2*a)).real  
  sol2 = ((-b+cmath.sqrt(d))/(2*a)).real

  # if they are floats, we need integers
  sol1 = math.ceil(sol1)
  sol2 = math.ceil(sol2)

  if sol1 > sol2:
    temp = sol1
    sol1 = sol2
    sol2 = temp

  return sol1, sol2

def main():
  # read input for part1
  with open(sys.argv[1], 'r') as file:
    times_pt1 = file.readline().split(':')[1].strip().split()
    distances_pt1 = file.readline().split(':')[1].strip().split()

  # parse input for part2
  time_pt2 = ''
  distance_pt2 = ''
  for time, distance in zip(times_pt1, distances_pt1):
    time_pt2+=time
    distance_pt2+=distance
  
  # convert to integers
  times_pt1 = list(map(int, times_pt1))
  distances_pt1 = list(map(int, distances_pt1))

  time_pt2, distance_pt2 = int(time_pt2), int(distance_pt2)

  # contains the results
  result_product_pt1 = result_product_pt2 = 1

  # iterate over races
  """
  Key idea here is to use r = number of seconds that we hold the button = speed of the boat
  n = # of time given in the race

  We essentially need to optimize speed * time = r * (n-r)
  Specifically, we need r * (n - r) > d, where d is the distance to beat
  Thus we are solving the quadratic of the form -r^2 + n*r -d = 0
  The roots will give us the minimum and maximum value that we can hold the button and still win the race

  The difference of these roots gives us the number of ways that we can beat the race
  """
  for time, distance in zip(times_pt1, distances_pt1):
    sol1, sol2 = get_roots(time, distance)

    # if this quantity is enough, we can multiply our product by the necessary quantity
    if sol1 * (time - sol1) > distance:
      result_product_pt1 *= (sol2 - sol1)
    # else if it isn't enough, lets increment our first root, and it will be enough
    elif (sol1 + 1) * (time - sol1 - 1) > distance:
      result_product_pt1 *= (sol2 - sol1 - 1)


  # do the same for part2
  sol1, sol2 = get_roots(time_pt2, distance_pt2)

  if sol1 * (time_pt2 - sol1) > distance_pt2:
    result_product_pt2 = (sol2 - sol1)
  # else if it isn't enough, lets increment our first root, and it will be enough
  elif (sol1 + 1) * (time_pt2 - sol1 - 1) > distance_pt2:
    result_product_pt2 = (sol2 - sol1 - 1)



  print(f'Answer to part 1: {result_product_pt1}')
  print(f'Answer to part 2: {result_product_pt2}')


if __name__ == '__main__':
  main()
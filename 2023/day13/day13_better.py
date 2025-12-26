import sys

def read_input():
  with open(sys.argv[1], 'r') as file:
    sections = file.read().strip().split('\n\n')
  return sections

def find_mirror_pt1(section):
  for r in range(1, len(section)):
    # get sub section above and below potential mirror
    # reverse the top arbitrarily (could be bottom also)

    # allows for ease of comparison of corresponding rows
    above = section[:r][::-1]
    below = section[r:]

    # this truncates both of them to the same length
    above = above[:len(below)]
    below = below[:len(above)]

    if above == below:
      return r

  return 0

def find_mirror_pt2(section):
  for r in range(1, len(section)):
    # get sub section above and below potential mirror
    # reverse the top arbitrarily (could be bottom also)

    # allows for ease of comparison of corresponding rows
    above = section[:r][::-1]
    below = section[r:]

    # this truncates both of them to the same length
    above = above[:len(below)]
    below = below[:len(above)]

    """
    sum( # sum all the hamming distances
      sum(0 if c_a == c_b else 1 # finding the hamming distance
            for c_a, c_b in zip(row_a, row_b))  # iterate over corresponding character
          for row_a, row_b in zip(above, below) # iterate over corresponding rows
      )
    """
    # essentially if the sum of all hamming distances is 1, then its a smudge and we can return the mirror
    if sum(sum(0 if c_a == c_b else 1 for c_a, c_b in zip(row_a, row_b)) for row_a, row_b in zip(above, below)) == 1:
      return r

  return 0



def main():
  sections = read_input()

  for pt, find_mirror in enumerate([find_mirror_pt1, find_mirror_pt2]):
    total = 0
    for i, section in enumerate(sections):
      section = section.splitlines()
      
      # Check for mirror in the rows, if its valid, add to the result and continue
      ref_point = find_mirror(section)
      if ref_point:
        total += (100 *ref_point)
        continue

      # else, transpose and check in the columns
      section = list(zip(*section))
      ref_point = find_mirror(section)
      total += ref_point
    
    print(f'Answer to part {pt}: {total}')


if __name__ == "__main__":
  main()

import sys

def read_input():
  with open(sys.argv[1], 'r') as file:
    sections = file.read().strip().split('\n\n')
  return sections


def find_mirror(section):
  '''
  Find 2 adjacent rows that are identical, and then verify that that location is a mirror
  if so return the point at which it is a mirror, if not return None
  '''

  # Find all possible mirror points
  potential_mirrors = []
  i = 0
  for j in range(1, len(section)):
    if section[i] == section[j]:
      potential_mirrors.append((i, j))
    i += 1
  
  # Verify if one is a mirror
  # if so return it
  # if its not, break and return None
  for i, j in potential_mirrors:
    res = i
    while i >= 0 and j < len(section):
      if section[i] != section[j]:
        break
      i, j = i - 1, j + 1 
    else:
      return (res + 1)
  
def main():
  sections = read_input()

  total = 0
  for i, section in enumerate(sections):
    section = section.splitlines()
    
    # Check for mirror in the rows, if its valid, add to the result and continue
    ref_point = find_mirror(section)
    if ref_point:
      total += (100 *ref_point)
      continue

    # else, transpose and check in the columns
    section = [''.join(line) for line in zip(*section)]
    ref_point = find_mirror(section)
    total += ref_point
  
  print(f'Answer to part 1: {total}')


if __name__ == "__main__":
  main()

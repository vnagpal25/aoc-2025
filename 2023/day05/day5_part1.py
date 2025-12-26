import sys

def main():
  # reads input
  with open(sys.argv[1], 'r') as file:
    sections = file.read().split("\n\n")
  
  # splits seeds and rest of sections
  seeds, *sections = sections

  # converts seeds string to array of ints
  seeds = list(map(int, seeds.split(":")[1].split()))

  # iterates over each section
  # the big idea here to determine a new set of 'seeds' for each section
  # that is, given the list of seeds, transform it into a new list of transformed seeds
  # corresponding to the mapping
  # for example if we start with the seeds, the first set of new seeds will be soil
  # and so on until locations
  for section in sections:
    # read the ranges into memory
    ranges = []
    for line in section.splitlines()[1:]:
      ranges.append(list(map(int, line.split())))
    
    # new seeds
    new_seeds = []
    
    # for each seed, determine the newly mapped seed
    for seed in seeds:
      # check each range
      for dest_st, source_st, length in ranges:
        # bingo, we found a range. append new mapping and break
        if seed in range(source_st, source_st + length):
          new_seeds.append(dest_st + seed - source_st)
          break
      else:
        # we never found a range. append the original seed
        new_seeds.append(seed)
    
    # transform seeds for next section
    seeds = new_seeds
  
  # seeds is now a list of locations, just get the minimum location now
  print(f'Answer to part 1: {min(seeds)}')


if __name__=="__main__":
  main()
  


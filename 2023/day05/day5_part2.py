import sys
def main():
  # read input
  with open(sys.argv[1], 'r') as file:
      sections = file.read().split("\n\n")

  # seperate inputs(seed ranges) from other sections
  inputs, *sections = sections
  inputs = list(map(int, inputs.split(":")[1].split()))

  # calculate seed ranges
  seed_ranges = []
  for i in range(0, len(inputs), 2):
      seed_ranges.append((inputs[i], inputs[i] + inputs[i + 1]))


  # iterate over each section
  # similar logic to part 1.
  # We are trying to transform each seed range (instead of an individual seed) to a new mapping now
  # at the end we will have a list of all the location ranges and we will pick the minimum from that
  for section in sections:
      # extract ranges
      ranges = []
      for line in section.splitlines()[1:]:
          ranges.append(list(map(int, line.split())))

      # will contain the new mappings
      new_seed_ranges = []

      # while loop here to handle cases where there isn't a 1-1 mapping between ranges
      # then we need to chop up a range into seperate sections and handle it
      # check seed_ranges.append() line for more information
      while seed_ranges:
          # this is the range that we are trying to map
          start_seed, end_seed = seed_ranges.pop()

          # check to see which range maps
          for dest_st, source_st, length in ranges:
              # we will do this by checking overlaps
              # drawing a picture for this part helps
              premapped_start = max(start_seed, source_st)
              premapped_end = min(end_seed, source_st + length)
              
              # there is some overlap, at least the overlapped section can be mapped
              if premapped_start < premapped_end: 
                  # - source_st + dest_st is the transformation or map being applied to the range
                  new_seed_ranges.append((premapped_start - source_st + dest_st, premapped_end - source_st + dest_st))
                  
                  # but we didn't consider the parts outside of the overlapped region
                  # if the overlap started after the start of the original range
                  # We need to still map the range to the left of the overlapped region
                  # we consider this by appending the non overlapped region back to the unmapped seeds list
                  if start_seed < premapped_start:
                      seed_ranges.append((start_seed, premapped_start))
                  # if the overlap ended before the end of the original range
                  # We need to still map the range to the right of the overlapped region
                  if end_seed > premapped_end:
                      # We still need to map the range to the right of the overlap
                      seed_ranges.append((premapped_end, end_seed))
                  break # since we found a mapping, we can break
          # no range mapped, so just append the original range
          else:
              new_seed_ranges.append((start_seed, end_seed))

      # new mapping for next section
      seed_ranges = new_seed_ranges

  # seed ranges now contains all of the location ranges
  # if we sort it and take the first element, we get the smallest range
  # if we take the start of that range we have our answer
  seed_ranges = sorted(seed_ranges)
  print(f'Answer to part 2: {min(seed_ranges[0])}')


if __name__ == "__main__":
    main()
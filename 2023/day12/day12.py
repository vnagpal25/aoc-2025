import sys

# cache prevents repeated calculations
spring_config_cache = {}

def count(springs, group_sizes):
  # Base Cases for Recursion

  # if there are no springs left, there better be 0 numbers left to satisfy
  if springs == "":
    return 1 if group_sizes == () else 0

  # if there are no numbers left to satisfy, we must not have any unoperational springs
  if group_sizes == ():
    return 1 if "#" not in springs else 0


  # if not cached, we need to calculate it
  if (springs, group_sizes) not in spring_config_cache:
    # counts number of configurations
    result = 0

    # First spring is either for sure operational or could be operational
    # either way the group sizes remain the same as there is no unoperational springs 
    # to be counted.  
    # so remove this character and count the rest of the valid configurations
    if springs[0] in ".?":
      result += count(springs[1:], group_sizes)

    # First spring is either unoperational or could be unoperational
    if springs[0] in "#?":
      # we will only count more if 3 conditions are met
      # - we have enough springs to meet the condition
      # - the next {num_req} springs are not "."
      # - the {num_req + 1} is not "#"

      num_req = group_sizes[0] 
      if num_req <= len(springs) and '.' not in springs[:num_req]  and(num_req == len(springs) or springs[num_req]!='#'):
        result += count(springs[num_req + 1:], group_sizes[1:])
    
    # store result in cache
    spring_config_cache[(springs, group_sizes)] = result
  
  # return cached result
  return spring_config_cache[(springs, group_sizes)]

def main():
  with open(sys.argv[1], 'r') as file:
    records = file.read().strip().splitlines()

  result_pt1 = 0
  result_pt2 = 0
  for record in records:
    # Part 1
    springs, group_sizes = record.split()
    group_sizes = tuple(map(int, group_sizes.split(",")))
    result_pt1 += count(springs, group_sizes)

    # Part 2
    group_sizes *= 5
    springs = '?'.join([springs] * 5)
    result_pt2 += count(springs, group_sizes)

  print(f'Part 1 result: {result_pt1}')
  print(f'Part 2 result: {result_pt2}')
if __name__ == '__main__':
  main()

from collections import defaultdict
# read input
with open('input.txt', 'r') as file:
  lines = file.readlines()
  lines = [line.strip() for line in lines if line!='\n']


def get_seed_numbers():
  # return seed numbers as a list (part 1)
  seeds = lines[0][lines[0].find(':') + 1: ].strip().split()
  seeds = list(map(int, seeds))
  return seeds


def get_seed_ranges():
  # return seed ranges as a list (part 2)
  seed_list = lines[0][lines[0].find(':') + 1: ].strip().split()
  seed_ranges = []
  i = 0
  while i < len(seed_list) - 1:
    start, length = int(seed_list[i]), int(seed_list[i + 1])
    seed_ranges.append((start, start + length - 1))
    i += 2
  return seed_ranges


def get_maps_unparsed():
  """
  Returns unparsed maps
  For example {seed-to-soil map: ['50 98 2', '52 50 48'], ...}
  """
  maps = defaultdict(list)
  
  i = 1
  while i < len(lines):
    curr_line = lines[i]
    if not lines[i][0].isdigit():
      i += 1
      while i < len(lines) and lines[i][0].isdigit(): 
        maps[curr_line[:-1]].append(lines[i])
        i += 1
  
  return maps


def get_maps_parsed(maps_unparsed):
  """
  Returns parsed maps which is 
  {seed-to-soil map: {(98, 99) : (50, 51),  (50, 97) : (52, 99)}, ...}
  """
  updated_maps = {key: None for key in maps_unparsed.keys()}
  
  for key, val in maps_unparsed.items():
    range_map = {}
    for three_tuple in val:
      three_tuple = list(map(int, three_tuple.split()))
      dest_start, source_start, length = three_tuple
      range_map[(source_start, source_start + length - 1)] = (dest_start, dest_start + length - 1)
    
    updated_maps[key] = range_map
  return updated_maps


def get_value(dict, goal_key):
  # dict = {(x, y): (a, b)}
  for key in dict.keys():
    if key[0] <= goal_key <= key[1]:
      return goal_key + (dict[key][0] - key[0])
  
  return goal_key


def get_location(parsed_maps, seed):
  # by traversing through different maps, we return the location
  soil = get_value(parsed_maps['seed-to-soil map'], seed)
  fert = get_value(parsed_maps['soil-to-fertilizer map'], soil)
  water = get_value(parsed_maps['fertilizer-to-water map'], fert)
  light = get_value(parsed_maps['water-to-light map'], water)
  temp = get_value(parsed_maps['light-to-temperature map'], light)
  humdty = get_value(parsed_maps['temperature-to-humidity map'], temp)
  loc = get_value(parsed_maps['humidity-to-location map'], humdty)
  return loc


def get_seed(inverse_maps, location):
  """
  By traversing through an inverse transformation, we return a seed number based on a given location
  """
  humdty = get_value(inverse_maps['humidity-to-location map'], location)
  temp =   get_value(inverse_maps['temperature-to-humidity map'], humdty)
  light =  get_value(inverse_maps['light-to-temperature map'], temp)
  water =  get_value(inverse_maps['water-to-light map'], light)
  fert =   get_value(inverse_maps['fertilizer-to-water map'], water)
  soil =   get_value(inverse_maps['soil-to-fertilizer map'], fert)
  seed =   get_value(inverse_maps['seed-to-soil map'], soil)
  return seed


def get_answer_part1(parsed_maps):
  """
  Returns answer to part 1
  """
  seeds = get_seed_numbers()
  min_location = float('inf')  
  for seed in seeds:

    location = get_location(parsed_maps, seed)
    
    min_location = min(min_location, location)
  return min_location


def get_answer_part2(inverse_maps):
  """Return answer to part 2 (failed attempt to reverse iterate)"""
  seed_ranges = get_seed_ranges()
  min_location = 0
  while True:
    print(f'Trying {min_location}')
    seed_num = get_seed(inverse_maps, min_location) 
    for seed_range in seed_ranges:
      if seed_range[0] <= seed_num <= seed_range[1]:
        return min_location
    min_location += 1


def get_maps_reversed(parsed_maps):
  """Reverses a mapping for each given range map"""
  for key, val in parsed_maps.items():
    new_val = {}
    for source_range, dest_range in val.items():
      new_val[dest_range] = source_range
    parsed_maps[key] = new_val
  return parsed_maps


def main():
  unparsed_maps = get_maps_unparsed()  
  parsed_maps = get_maps_parsed(unparsed_maps)
  # reversed_maps = get_maps_reversed(parsed_maps)

  min_location_pt1 = get_answer_part1(parsed_maps)
  # min_location_pt2 = get_answer_part2(reversed_maps)

  print(f'Answer to part 1: {min_location_pt1}')
  # print(f'Answer to part 2: {min_location_pt2}')


if __name__=="__main__":
  main()
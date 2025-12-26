import sys


def accept(boolean, part):
  """
  Checks if a boolean condition is true or not
  """
  if '>' in boolean:
    style, thresh = boolean.split('>')
    return part[style] > int(thresh)
  else: # < in boolean
    style, thresh = boolean.split('<')
    return part[style] < int(thresh)


def determine_good_part(part, workflows):
  # start at 'in'
  start = workflows['in']
  
  # loop until we return
  while True:
    # loop through each rule
    for rule in start:
      if ':' in rule:
        # boolean condition needs to be checked
        boolean, dest = rule.split(':') 

        # if the boolean condition is true, we need to go to that destination
        if accept(boolean, part):

          # accept or reject
          if dest in 'AR':
            return dest
          
          # set new start and break from current rules loop
          start = workflows[dest]
          break
      
      else:
        # accept or reject
        if rule in 'AR':
          return rule

        # set new start
        start = workflows[rule]


def read_input():
  with open(sys.argv[1], 'r') as file:
    # splitting workflow information and parts information
    w, p = file.read().split('\n\n')
    
    # create a hashmap of worflow names to a list of rules
    w = w.splitlines()
    workflows = {}
    for workflow in w:
      name, rules = workflow.split('{')
      rules = rules[:-1]
      workflows[name] = rules.split(',')

    # create an array of hashmaps (each containining keys in 'xmas' and values in (1, 4000))
    p = p.splitlines()
    parts = []
    for part in p:
      part = part[1:-1]
      xmas = part.split(',')
      hashmap = {}
      for rating in xmas:
        type_, rating_ = rating.split('=')
        hashmap[type_] = int(rating_)
      
      parts.append(hashmap)
  
  # return parsed input
  return parts, workflows


def part1(parts, workflows):
  total = 0

  for part in parts:
    # if accepted, add to the total sum
    if determine_good_part(part, workflows) == 'A':
      total += sum(part.values())
    
  print(f'Total part 1: {total}')



def count(ranges, workflows, start = 'in'):
  # Recursion Base Cases
  if start == 'R':
    # Invalid configurations
    return 0
  
  if start == 'A':
    # Valid configurations
    # count all of the distinct configurations given by the ranges
    product = 1
    for lo, hi in ranges.values():
      product *= (hi - lo + 1)
    return product

  # Recursive Calls
  # set total to 0
  total = 0

  # get list of rules and iterate over them
  rules = workflows[start]
  for rule in rules:
    # boolean condition is in the rule
    if ':' in rule:
      condition, dest = rule.split(':')
      if '<' in condition:
        # < condition
        # Break into True range (all the values for which this condition is true)
        # and        False range (all the value for which this condition is false)
        key, thresh = condition.split('<')
        thresh = int(thresh)
        lo, hi = ranges[key]

        # all the values for which it is true
        T_range = (lo, thresh - 1)

        # all the values for which it is false
        F_range = (thresh, hi)
      else:
        # > in condition
        key, thresh = condition.split('>')
        thresh = int(thresh)
        lo, hi = ranges[key]
        
        # all the value for which it is true
        T_range = (thresh + 1, hi)

        # all the values for which it is false
        F_range = (lo, thresh)
      
      # make recursive call for T_range: send them to the dest
      if T_range[0] <= T_range[1]:
        # valid T range
        # new ranges dict
        new_ranges = dict(ranges)
        new_ranges[key] = T_range

        # count all configurations with new ranges
        total += count(new_ranges, workflows, dest)
      
      if F_range[0] <= F_range[1]:
        # valid F range, need to continue in this same loop so update the current ranges dict
        # in subsequent iterations, we will count the number of configurations with update range
        ranges = dict(ranges)
        ranges[key] = F_range

    else:
      # fallback rule
      total += count(ranges, workflows, rule)
  
  return total


def part2(workflows):
  # these are all of the ranges that we need to check
  # will chose an interval math approach instead of looping over 4000 ^ 4 distinct configurations
  ranges = {key:(1, 4000) for key in 'xmas'}
  print(f'Total for part 2: {count(ranges, workflows)}')


def main():
  parts, workflows = read_input()
  
  part1(parts, workflows)

  part2(workflows)

if __name__ == "__main__":
  main()
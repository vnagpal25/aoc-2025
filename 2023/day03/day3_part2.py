import math

# Read input and strip newline character in each line
with open('input.txt', 'r') as file:
  lines = file.readlines()
  lines = [line.strip() for line in lines]


def product(numbers):
  """
  Returns the product of a set of numbers
  """
  return math.prod(numbers)


def find_gear_indices():
  """
  Returns all of the indices where there is a '*'
  """
  gear_indices = []
  for i, line in enumerate(lines):
    for j, char in enumerate(line):
      if char == "*":
        gear_indices.append((i, j))
  return gear_indices


def contains_number(i, j):
  """
  Returns true if the position in the lines array contains a number 
  False otherwise
  """
  # if not a digit, return
  if not lines[i][j].isdigit():
    return False, None
  
  # else current character is a digit 

  # get the beginning of the number (search leftwards)
  left = j
  while left >= 1 and lines[i][left - 1].isdigit():
    left -= 1
  
  # get the end of the number (search rightwards)
  right = j
  while right < len(lines[0]) - 1 and lines[i][right + 1].isdigit():
    right += 1
  
  # return True and the number itself
  return True, int(lines[i][left : right + 1])


def gear_product(g_row, g_col):
  """
  Returns the gear product of the gear specified by the input location
  Refer to the problem constraints for more details
  """

  # 8 possible locations where a number could be
  possible_locations = [(g_row - 1, g_col), (g_row + 1, g_col), 
                        (g_row, g_col - 1), (g_row, g_col + 1), 
                        (g_row - 1, g_col - 1), (g_row + 1, g_col + 1), 
                        (g_row - 1, g_col + 1), (g_row + 1, g_col - 1)]
  
  # hashset prevents duplicate elements from being added
  numbers = set()

  # iterates over possible locations
  for pos in possible_locations:
    i, j = pos

    # checks if the location is valid
    if (0 <= i <= len(lines) - 1) and (0 <= j <= len(lines[0]) - 1):
      # checks if the position contains a number
      has_number, number = contains_number(i, j)
      
      # if it does, add it to the set
      if has_number:
        numbers.add(number)
      
      # check if there are more than two numbers, if so return 0
      if len(numbers) > 2:
        return 0
  
  # return true iff there are only two numbers adjacent to the gear
  # else return 0
  return product(numbers) if len(numbers) == 2 else 0


def main():
  # find all indices of gears (*)
  gear_indices = find_gear_indices()
  
  sum_pt2 = 0
  # determine if those asterisks(gears) are adjacent to EXACTLY two numbers
  for gear_index in gear_indices:
    # add the gear product for each gear (zero or nonzero)
    sum_pt2 += gear_product(*gear_index)

  print(f'Answer to part 2: {sum_pt2}')


if __name__ == "__main__":
  main()
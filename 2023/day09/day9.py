def monotone_pattern(pattern):
  """
  Checks if a pattern is monotone (i.e., not increasing nor decreasing)
  """
  for i in range(len(pattern) - 1):
     if pattern[i + 1] - pattern[i] != 0:
       return False
  return True


def get_diff_pattern(pattern):
  """
  Returns the difference pattern of each pattern
  For example, if pattern = [a_1,       a_2,       ..., a_n]
  Then,              diff = [a_2 - a_1, a_3 - a_2, ..., a_n - a_(n-1)]
  """
  diff = []
  for i in range(len(pattern) - 1):
    diff.append(pattern[i + 1] - pattern[i])

  return diff


def get_next_value(pattern):
  """
  Gets the next value in a pattern
  """

  # keeps track of the last value of each pattern
  last_values = []

  # calculates the difference pattern iteratively until its monotone
  while not monotone_pattern(pattern):
    last_values.append(pattern[-1])
    pattern = get_diff_pattern(pattern)

  # the monotone pattern determines the next value of the immediately preceding pattern(which we keep track of using last vlaues)
  # using these stored values, we can keep iteratively calculate the next value of each difference sequence
  incrementer = pattern[0]
  for last_val in last_values[::-1]: # reverse because we are building it from the bottom up
    incrementer = last_val + incrementer

  # the last value of incrementer is the next value of the inputted sequence
  return incrementer


def main():
  # read input
  with open('input.txt', 'r') as file:
    patterns = file.readlines()
  
  # holds the sum of all of the next values and all of the previous values
  next_sum = 0
  prev_sum = 0


  for pattern in patterns:
    # splits by spaces and converts all strings to ints
    pattern = pattern.split()
    pattern = [int(num) for num in pattern]

    # gets the next value and previous value for each pattern and adds it to the total sum
    next_sum += get_next_value(pattern)

    # the previous value in the pattern is the same as the next value of the pattern in reverse 
    prev_sum += get_next_value(pattern[::-1])

  print(f'Sum of all next values: {next_sum}')
  print(f'Sum of all previous values: {prev_sum}')


if __name__ =="__main__":
  main()

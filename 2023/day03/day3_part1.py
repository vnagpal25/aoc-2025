# Read input and strip newline character in each line
with open('input.txt', 'r') as file:
  lines = file.readlines()
  lines = [line.strip() for line in lines]


def contains_symbol(sub_line):
  """
  Checks if a string contains a symbol aka 
  a character that is not a period or a digit
  """
  for char in sub_line:
    if not (char == '.' or char.isdigit()):
      return True

  return False


def get_right_index(line, left_index):
  """
  Given the left index of a number and the line the number is in,
  return the right index of that number
  """
  for i in range(left_index, len(line)):
    # reached a non digit, so return the previous index
    if not line[i].isdigit(): 
      return i - 1
  # we reached the end of the line, so return the last index
  return len(line) - 1 


def get_number_indices():
  """
  Returns a list of all location tuples corresponding to numbers
  For clarity: 3-tuple = (row index, left column number, and right column number)
  """

  # holds 3 -tuples
  number_indices = []

  # iterate over the lines
  for i, line in enumerate(lines):

    # iterate within the line
    j = 0
    while j < len(line):
      # get the current character
      char = line[j]
      # if it is a digit, append its indices and skip to the next character past it
      if char.isdigit():
        right_index = get_right_index(line, j) # get right column
        number_indices.append((i, j, right_index)) # append result
        j = right_index + 1  # skip past
      else:
        j += 1 # simply keep incrementing
  
  # return result
  return number_indices


def is_adjacent_to_symbol(i, j_l, j_r):
  """
  Given the index of a number within the lines list
  Return true if it is adjacent to a symbol, false otherwise

  Consider the number to be the following (for simplicity of notation, I am writing lines[i][j] as l_ij):
  l_(i,j_l) ... l_(i,j_r)

  Now there are 2 * (j_r - j_l + 1) + 6 spots where there could be a symbol

  There are at least 6 spots because of the character
    - to the left                       (i, j_l - 1)
    - to the right                      (i, j_r + 1)
    - to the left and up    (northwest) (i - 1, j_l - 1)
    - to the left and down  (southwest) (i + 1, j_l - 1)
    - to the right and up   (northeast) (i - 1, j_r + 1)
    - to the right and down (southeast) (i + 1, j_r + 1)
  
  There are at least 2 * (j_r - j_l + 1) spots because of the
    - line directly above the number (j_r - j_l + 1) spots
    - line directly below the number (j_r - j_l + 1) spots
  """
  # Checking easy 6
  easy_adjacent_indices = [(i, j_l - 1), (i, j_r + 1),
                           (i - 1, j_l - 1), (i + 1, j_l - 1),
                           (i - 1, j_r + 1), (i + 1, j_r + 1)]

  for index_pair in easy_adjacent_indices:
    row_num, col_num = index_pair
    # valid row, valid col, not a period or digit defines a symbol
    if (0<=row_num < len(lines)) and (0<=col_num < len(lines[0])) and not(lines[row_num][col_num] == '.' or lines[row_num][col_num].isdigit()):
      return True

  # Checking line above
  if i - 1 >= 0 and contains_symbol(lines[i - 1][j_l: j_r + 1]):
    return True

  # Checking line below
  if i + 1 < len(lines) and contains_symbol(lines[i + 1][j_l: j_r + 1]):
    return True

  # alas to no avail, return False
  return False


def main():
  # get the list of number indices
  number_indices = get_number_indices()

  sum_pt1 = 0 # sum for part 1

  # iterate over all possible number locations
  for number_index_tuple in number_indices:
    # unpack the tuple
    row_num, left_col, right_col = number_index_tuple

    # figure out if the number is adjacent to a symbol
    # if so, add the number
    if is_adjacent_to_symbol(row_num, left_col, right_col):
      sum_pt1 += int(lines[row_num][left_col: right_col + 1])

  print(f'Answer to part 1: {sum_pt1}')


if __name__ == "__main__":
  main()

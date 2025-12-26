import math

# constraint from part 1
# legal games are the games that have at most this many
max_colors = {'red': 12, 'green': 13, 'blue': 14}


def power(colors_map):
  """
  Returns the product of a dictionary's values
  """
  return math.prod(colors_map.values())


def valid_game(colors_map):
  """
  Based on the constraints of part 1, returns if the played game was legal or not
  """
  for color, allowed_num in max_colors.items():
    if colors_map[color] > allowed_num:
      return False
  return True


def parse_line(line):
  """
  Parses a line and returns the game number and 
  the maximum amount of each marble required to play the particular game
  """

  # Finds the game number as between the first 'e' and the first ':'
  game_number = int(line[line.find('e') + 1: line.find(':')])

  # subsets are seperated by semicolons
  subsets = line[line.find(':') + 1:].split(';')

  # to return, will contain the maximum amount of each color required to play the game
  max_colors = {'red': 0, 'green': 0, 'blue': 0}

  # iterates over each of the subsets in a game
  for subset in subsets:
    # within each subset, different color counts are seperated by commas
    diff_colors = subset.split(',')

    for diff_color in diff_colors:
      # strips off white spaces from ends
      diff_color = diff_color.strip()

      # number and color are seperated by a space
      num, color = diff_color.split()

      # computes the new required maximum
      max_colors[color] = max(max_colors[color], int(num))

  return game_number, max_colors


def main():
  # Reads input
  with open("input.txt", 'r') as file:
    lines = file.readlines()

  # sum for each part
  sum_pt1 = 0
  sum_pt2 = 0

  # iterates over the lines
  for line in lines:
    # parses each line
    id, max_colors = parse_line(line)

    # if valid, updates the sum value for part 1
    if valid_game(max_colors):
      sum_pt1 += id

    # update the sum value for part 2
    sum_pt2 += power(max_colors)

  print(f'Answer to part 1: {sum_pt1}')
  print(f'Answer to part 2: {sum_pt2}')


if __name__ == "__main__":
  main()

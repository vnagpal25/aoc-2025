# Read input
with open('input.txt', 'r') as file:
  lines = file.readlines()

# initialize hashmap that keeps track of how many of each card we currently have
# starting off we have 1 of each card
card_counts = {card_num: 1 for card_num in range(1, len(lines) + 1)}


def parse_line(line):
  """
  Parses a line and returns two lists: one of winning numbers and one of playing numbers
  """
  # remove beginning portion
  line = line[line.find(':') + 1:]

  # get the winning numbers and the player numbers
  # strip whitespaces and split by seperating spaces into a list
  win_nums = line[: line.find('|')].strip().split()
  play_nums = line[line.find('|') + 1:].strip().split()

  # convert all to ints
  win_nums = [int(num) for num in win_nums]
  play_nums = [int(num) for num in play_nums]

  return win_nums, play_nums


def get_points_pt1(win_nums, play_nums):
  """
  Returns the amount of points we get from a particular card
  based on the numbers recieved and the winning number
  """
  # initial score is 0
  score = 0

  # convert winning numbers into a hashset O(n) time
  # O(n) memory also
  win_nums = set(win_nums)

  # iterate over played numbers O(m) time
  for num in play_nums:

    #check membership in the winning numbers O(1)
    if num in win_nums:
      if not score:
        # if this is our first match, then the score is one
        score = 1
      else:
        # else we double our score
        score *= 2

  # overall this is O(n + m) time and O(n) space
  return score


def update_cards_won_pt2(win_nums, play_nums, card_num):
  """
  Based on the inputted card, update how many cards we have won overall for part 2
  """

  # convert winning numbers to a hashset O(n) space and time
  win_nums = set(win_nums)

  # current number of card won
  card_won_number = card_num

  for num in play_nums:
    # check if it is winning number
    if num in win_nums:
      # first increment the winning card number
      # for example if our card number is 1 and we found a match, we win a copy of 1+1 = 2
      card_won_number += 1

      # check that we are not overflowing or cards
      if card_won_number <= len(lines):
        # If we have 1 match on card 2 and we have x copies of card 2, 
        # we win x copies of card 3
        card_counts[card_won_number] += card_counts[card_num]


def main():
  # sum for part 1
  sum_pt1 = 0

  # iterate over lines
  for i, line in enumerate(lines):
    # parse the input into two lists: winning numbers and played numbers
    win_nums, play_nums = parse_line(line)

    # get the points won from part 1
    sum_pt1 += get_points_pt1(win_nums, play_nums)

    # update the cards won for part 2
    update_cards_won_pt2(win_nums, play_nums, i+1)

  print(f'Answer to part 1: {sum_pt1}')
  print(f'Answer to part 2: {sum(card_counts.values())}')


if __name__ == "__main__":
  main()

# Necessary Libraries
import sys
from collections import Counter

# Merge sort for breaking ties within a category
from merge_sort import merge_sort

# Order preference for part 1
order = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9, '9': 8,
             '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}


def main():
  # read iput
  with open(sys.argv[1], 'r') as file:
    lines = file.readlines()

  # parse input
  lines = [line.split() for line in lines]
  bids_map = {card: int(bid) for card, bid in lines}

  # contains all of the different winning categories
  five_of_a_kind, four_of_a_kind, full_house = [], [], []
  three_of_a_kind, two_pair = [], []
  one_pair, high_card = [], []
  category_rankings = [five_of_a_kind, four_of_a_kind,
                       full_house, three_of_a_kind, two_pair, one_pair, high_card]

  # iterates over cards
  for card in bids_map.keys():
    # hashmap determines the type of hand
    card_map = Counter(card)

    # different card counts
    counts = list(card_map.values())

    # self explanatory
    if 5 in counts:
      five_of_a_kind.append(card)
    elif 4 in counts:
      four_of_a_kind.append(card)
    elif 3 in counts and 2 in counts:
      full_house.append(card)
    elif 3 in counts:
      three_of_a_kind.append(card)
    elif counts.count(2) == 2:
      two_pair.append(card)
    elif counts.count(2) == 1:
      one_pair.append(card)
    else:
      high_card.append(card)

  # all rankings contains a list of all the hands
  all_rankings = []
  for ranking_list in category_rankings:
    # merge sort to break the ties
    merge_sort(ranking_list, 0, len(ranking_list) - 1, order)

    # append all of the hands to the big list
    all_rankings.extend(ranking_list)

  # iterate over the list backwards to determine the winnings
  total_winnings= 0
  for i, card in enumerate(all_rankings[::-1]):
    total_winnings += (i + 1) * bids_map[card]
  
  print(f'Total winnings: {total_winnings}')


if __name__ == "__main__":
  main()

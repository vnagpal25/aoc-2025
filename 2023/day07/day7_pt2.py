# Necessary Libraries
import sys
from collections import Counter

# Merge sort for breaking ties
from merge_sort import merge_sort


# Order preference for part 2
order = {'A': 13, 'K': 12, 'Q': 11, 'T': 10, '9': 9,
             '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1}

# Makes a hand strong using the joker wild cards
def make_card_strong(card_map):
  # 5 jokers edge case, return
  if card_map['J'] == 5:
    return card_map

  # if the joker is the most abundant card
  if card_map['J'] == max(card_map.values()):
    # the joker is the only card with the max value
    if list(card_map.values()).count(card_map.get('J', 0)) == 1:
      # iterate over the most significant cards(already specified in the 'order')
      # add the count of jokers to the max card
      # and return the updated map
      for key in order:
        if key in card_map:
          card_map[key] += card_map['J']
          card_map['J'] = 0
          return card_map
    else:
    # there is another card with the max value
    # find it, and add all of the jokers to it to make it as strong as possible
    # return the updated card map
      for key in order:
        if card_map.get(key, 0) == card_map['J']:
          card_map[key] += card_map['J']
          card_map['J'] = 0
          return card_map

  # Joker isn't the most abundant card, so find the most abundant card
  # and give it all of the jokers, return
  max_key = max(card_map, key=card_map.get)
  card_map[max_key] += card_map['J']
  card_map['J'] = 0
  return card_map

def main():
  with open(sys.argv[1], 'r') as file:
    lines = file.readlines()

  lines = [line.split() for line in lines]
  bids_map = {card: int(bid) for card, bid in lines}

  five_of_a_kind, four_of_a_kind, full_house = [], [], []
  three_of_a_kind, two_pair = [], []
  one_pair, high_card = [], []
  category_rankings = [five_of_a_kind, four_of_a_kind,
                       full_house, three_of_a_kind, two_pair, one_pair, high_card]

  for card in bids_map.keys():
    # get the card counts, and if there is a joker, make the hand strong
    card_map = Counter(card)
    if 'J' in card_map:
      card_map = make_card_strong(card_map)


    # same logic as part 1
    counts = list(card_map.values())
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

  # Same logic as part 1
  all_rankings = []
  for ranking_list in category_rankings:
    merge_sort(ranking_list, 0, len(ranking_list) - 1, order)
    all_rankings.extend(ranking_list)

  # Same logic as part 1
  total_winnings= 0
  for i, card in enumerate(all_rankings[::-1]):
    total_winnings += (i + 1) * bids_map[card]

  print(f'Total winnings: {total_winnings}')


if __name__ == "__main__":
  main()

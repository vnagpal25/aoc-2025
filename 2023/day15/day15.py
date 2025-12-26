import sys


def hash(sequence):
  current_value = 0
  for ch in sequence:
    current_value += ord(ch)
    current_value *= 17
    current_value %= 256
  return current_value


def main():
  with open(sys.argv[1], 'r') as file:
    init_seq = list(map(str.strip, file.read().split(',')))

  total_part2 = 0

  hashmap = {} # (hash_code : [box contents])
               # box contents = [label focal_length]
  for i, group in enumerate(init_seq):
    if '=' in group:
      label, focal_length = group.split('=') 
      box_num = hash(label)
      if box_num not in hashmap:
        hashmap[box_num] = {}
      if label in hashmap[box_num]:
        i_old, _ = hashmap[box_num][label]
        hashmap[box_num][label] = (i_old, focal_length)
      else:
        hashmap[box_num][label] = (i, focal_length)

    elif '-' in group:
      label = group.split('-')[0]
      box_num = hash(label)
      if box_num in hashmap and label in hashmap[box_num]:
        hashmap[box_num].pop(label)
  
  for box in hashmap:
    if hashmap[box]:
      lenses = hashmap[box]
      sorted_lenses = sorted(lenses.values(), key=lambda x: x[0])
      sorted_lenses = [x[1] for x in sorted_lenses]
      for i, lens in enumerate(sorted_lenses):
        total_part2 += (box + 1) * (i + 1) * int(lens)
  print(f'Total for part 1: {sum(map(hash, init_seq))}')
  print(f'Total for part 2: {total_part2}')
  
if __name__=="__main__":
  main()
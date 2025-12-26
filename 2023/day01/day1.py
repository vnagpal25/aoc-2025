from trie import Trie
# Create a trie and insert words
words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
trie = Trie(words)
number_map = {"one":'1', "two":'2', "three":'3', "four":'4', "five":'5', "six":'6', "seven":'7', "eight":'8', "nine":'9'}


def find_calibration_val_pt1(line):
  num = ''
  for char in line:
    try: # creating a number string
      int(char)
      num += char
    except: # can't be converted to an int,ignore
      pass
  

  return int(num[0] + num[-1])


def find_calibration_val_pt2(line):
  num = ''
  current_letters = ''
  for char in line:
    # print(num, char, current_letters)
    try: # creating a number string
      int(char)
      num += char
    except:
      current_letters += char # add current char to the number set

      if not trie.search_prefix(current_letters):
        # trim the first character off if it is not a valid prefix
        # oni isn't a prefix, but ni is 
        current_letters = current_letters[1:] # covers cases like twonine, where 2 is counted, it tries to get 1 then fails, then gets 9
      
      elif trie.search_word(current_letters):
        # it is number, append it to our string
        num += number_map[current_letters]

        # reset to empty string
        current_letters = ''

        # handles overlapping case like twone or eightwo
        if trie.search_prefix(char):
          current_letters = char
  
  return int(num[0] + num[-1])



def main():
  # read input
  with open('input.txt', 'r') as file:
    lines = file.readlines()

  sum_calibration_vals_pt1 = 0
  sum_calibration_vals_pt2 = 0

  for i, line in enumerate(lines):
    sum_calibration_vals_pt1 += find_calibration_val_pt1(line)
    sum_calibration_vals_pt2 += find_calibration_val_pt2(line)
  
  print(f'Answer to part 1: {sum_calibration_vals_pt1}')
  print(f'Answer to part 2: {sum_calibration_vals_pt2}')

if __name__=="__main__":
  main()
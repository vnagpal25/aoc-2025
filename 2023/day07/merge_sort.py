def compare(s1: str, s2: str, order):

    if len(s1) == len(s2) == 1 and s1[0] == s2[0]:
      return 0
    elif order[s1[0]] > order[s2[0]]:
      return 1
    elif order[s1[0]] < order[s2[0]]:
      return -1
    else:
      return compare(s1[1:], s2[1:], order)


def merge(arr, l, m, r, order):
  left_arr = []
  right_arr = []
  left_arr.extend(arr[l:m+1])
  right_arr.extend(arr[m+1:r+1])

  i, j, k = 0, 0, l
  while i < len(left_arr) and j < len(right_arr):
    if compare(left_arr[i], right_arr[j], order) > 0:
      arr[k] = left_arr[i]
      k += 1
      i += 1
    else:
      arr[k] = right_arr[j]
      k += 1
      j += 1

  while i < len(left_arr):
    arr[k] = left_arr[i]
    i += 1
    k += 1
  while j < len(right_arr):
    arr[k] = right_arr[j]
    j += 1
    k += 1


def merge_sort(arr, l, r, order):
  if l < r:
    m = (l + r)//2
    merge_sort(arr, l, m, order)
    merge_sort(arr, m + 1, r, order)

    merge(arr, l, m, r, order)

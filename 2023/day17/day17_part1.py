import sys
from heapq import heappush, heappop # implements priority queue pushing and popping operations in the form of a minheap

def main():
  with open(sys.argv[1], 'r') as file:
    grid = [list(map(int, line.strip())) for line in file.readlines()]
  
  # Dijkstra's Algorithm

  seen = set() # keeps track of seen nodes

  # node is of the form (heat loss, row #, col #, delta row, delta col, steps taken)
  pq = [(0, 0, 0, 0, 0, 0)] 
  
  # keep exploring until we have paths to explore
  while pq:
    # pop the minimum element from the priority queue
    hl, r, c, dr, dc, n = heappop(pq)

    # check if we have reached the end
    if (r, c) == (len(grid) - 1, len(grid[0]) - 1):
      print(hl)
      break

    # check if out of bounds
    if r < 0 or r >= len(grid) or c < 0  or c>= len(grid[0]):
      continue

    # if seen continue
    if (r, c, dr, dc, n) in seen:
      continue
    
    # we are going to keep track of the location (r, c) and the direction we approached it (dr, dc)
    # as well as the number of steps taken n
    seen.add((r, c, dr, dc, n))

    # only add next node to the priority queue if we've taken less than 3 steps
    # and this is not the initial node 
    if n < 3 and (dr, dc) != (0, 0):
      # keep traversing in the same direction but increment the steps
      nr, nc = r + dr, c + dc
      if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
        heappush(pq, (hl + grid[nr][nc], nr, nc, dr, dc, n + 1))
    
    # check right, down, left, and up
    for ndr, ndc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
      # only explore if not the same direction (because that has already been pushed) 
      # and its not the reverse direction (because the crucible can't travel backwards) 
      if (ndr, ndc) not in [(dr, dc), (-dr, -dc)]:
        nr, nc = r + ndr, c + ndc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
          heappush(pq, (hl + grid[nr][nc], nr, nc, ndr, ndc, 1)) # 1 step because its the 1st step in that direction
              

if __name__ == "__main__":
  main()

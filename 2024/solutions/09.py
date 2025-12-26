import os
from typing import List
day: str = os.path.basename(__file__).split(
    '.')[0]  # name file between 01 and 25

test: str = """2333133121414131402"""
pt1_ans: int = 1928
pt2_ans: int = 2858


def parse_input(string: str):
    """Return physical diskmap with array representing contiguous memory"""
    disk_map = []
    for i, n in enumerate(string):
        if i % 2 == 0:
            # This is a file index, so we append n blocks of that file id
            disk_map += [i // 2] * int(n)
        else:
            # blank space, so we append n blocks of blank space
            disk_map += ['.'] * int(n)
    return disk_map


def parse_input_pt2(string: str):
    """Return diskmap with extra information about files and blanks"""
    files = {}  # map of form file_id:(starting position, length)
    blanks = []  # list of form (starting_position, length)

    pos = 0  # starting position of current object (file or blank stretch)
    for i, n in enumerate(string):
        n = int(n)

        # file
        if i % 2 == 0:
            files[i//2] = (pos, n)
        # blank
        else:
            if n != 0:  # only keep track of non empty blank space
                blanks.append((pos, n))
        pos += n  # increment past the file or blanks
    return files, blanks


def shift_disk_map(disk_map: List[int]):
    """Shift disk map by fragmenting memory"""
    # get all indices of blanks
    free_indices = [i for i, x in enumerate(disk_map) if x == '.']

    # for each blank from the left side of the memory, we move in files from the right side by fragmenting them
    for i in free_indices:
        # remove trailing blanks
        while disk_map[-1] == '.':
            disk_map.pop()

        # check if blank index is obsolete
        if len(disk_map) <= i:
            break

        #  move tail file portion to blank space
        disk_map[i] = disk_map.pop()
    return disk_map


def shift_disk_map_pt2(files, blanks: list):

    # starting from the last file, move it to the first blank portion large enough to have the entire file
    file_id = len(files) - 1
    while file_id >= 0:
        # get the file length and starting position
        file_pos, file_len = files[file_id]

        # searching for blank space large enough
        for i, (blank_pos, blank_len) in enumerate(blanks):
            # no blank before the file exists to move the file to, so we break out of this loop to move onto the next file
            if blank_pos >= file_pos:
                # in addition, disregard the blanks after this index as we can't move any of the remaining files further to the right in memory
                blanks = blanks[:i]
                break

            # found a spot large enough for the file
            if file_len <= blank_len:
                # move the file to the blank's starting position
                files[file_id] = (blank_pos, file_len)

                # perfect switch, we don't track the blank anymore
                if file_len == blank_len:
                    blanks.pop(i)
                # remaining space in the blank, so update its position
                else:
                    blanks[i] = (blank_pos+file_len, blank_len-file_len)
                break
        file_id -= 1
    return files


def pt1(disk_map):
    disk_map = shift_disk_map(disk_map)
    return sum(i * int(ch) for i, ch in enumerate(disk_map))


def pt2(files, blanks):
    files = shift_disk_map_pt2(files, blanks)
    return sum(i*x for i, (pos, size) in files.items()
               for x in range(pos, pos + size))


def main(puzzle: str):
    test_map = parse_input(test)
    disk_map = parse_input(puzzle)
    assert pt1_ans == pt1(test_map)
    print(f"Part 1: {pt1(disk_map)}")

    test_files, test_blanks = parse_input_pt2(test)
    files, blanks = parse_input_pt2(puzzle)

    assert pt2_ans == pt2(test_files, test_blanks)
    print(f"Part 2: {pt2(files, blanks)}")


if __name__ == "__main__":
    with open(f'puzzles/{day}.txt', 'r') as f:
        puzzle = f.read()
        main(puzzle)

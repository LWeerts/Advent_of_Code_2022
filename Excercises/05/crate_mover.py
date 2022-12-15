"""
Moves crates and returns the letters of the top crates in each stack

Advent of code day 05
"""

import copy


def parse_input(file):
    crates_done = False
    crates = []
    moves = []
    for line in file:
        if crates_done:  # Reading moves
            split_line = line.split()
            amount = int(split_line[1])
            origin = int(split_line[3]) - 1
            destination = int(split_line[5]) - 1
            moves.append((amount, origin, destination))

        elif line == "\n":  # End of crate section
            crates_done = True
            # Transpose crates
            new_crates = [[] for _ in range(len(crates[0]))]
            for row_of_crates in crates[::-1]:
                for ix, crate in enumerate(row_of_crates):
                    if crate == " ":
                        continue
                    new_crates[ix].append(crate)

        elif line.startswith("["): # Part of crate section
            num_crates = (len(line) + 1) // 4
            row_of_crates = []
            for ix in range(num_crates):
                row_of_crates.append(line[ix * 4 + 1])
            crates.append(row_of_crates)

    return new_crates, moves


def move_crates_single(crates, moves):
    for move in moves:
        # move crates from top of 1 stack to back of other stack one by one
        # thus reversing order
        for _ in range(move[0]):
            crates[move[2]].append(crates[move[1]].pop())
    return crates


def move_crates_multi(crates, moves):
    for move in moves:
        # move crates simultaniously, keeping order
        crates[move[2]].extend(crates[move[1]][-move[0]:])
        del crates[move[1]][-move[0]:]
    return crates


def grab_letters(crates):
    """grab letters of all top crates"""
    letters = []
    for stack_of_crates in crates:
        letters.append(stack_of_crates[-1])
    print("".join(letters))


def main():
    with open("input.txt") as file:
        crates, moves = parse_input(file)
        crates_1 = copy.deepcopy(crates)
    moved_crates_single = move_crates_single(crates, moves)
    moved_crates_multi = move_crates_multi(crates_1, moves)
    grab_letters(moved_crates_single)
    grab_letters(moved_crates_multi)


if __name__ == "__main__":
    main()

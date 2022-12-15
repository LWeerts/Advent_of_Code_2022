def parse_input(file):
    crates_done = False
    crates = []
    moves = []
    for line in file:
        if crates_done:
            split_line = line.split()
            amount = int(split_line[1])
            origin = int(split_line[3]) - 1
            destination = int(split_line[5]) - 1
            moves.append((amount, origin, destination))

        elif line == "\n":
            crates_done = True
            new_crates = [[] for _ in range(len(crates[0]))]
            for row_of_crates in crates[::-1]:
                for ix, crate in enumerate(row_of_crates):
                    if crate == " ":
                        continue
                    new_crates[ix].append(crate)

        elif line.startswith("["):
            num_crates = (len(line) + 1) // 4
            row_of_crates = []
            for ix in range(num_crates):
                row_of_crates.append(line[ix * 4 + 1])
            crates.append(row_of_crates)

    return new_crates, moves


def move_crates(crates, moves):
    for move in moves:
        for _ in range(move[0]):
            crates[move[2]].append(crates[move[1]].pop())
    return crates


def main():
    with open("input.txt") as file:
        crates, moves = parse_input(file)
        moved_crates = move_crates(crates, moves)
        # grab letters of all top crates
        letters = []
        for stack_of_crates in moved_crates:
            letters.append(stack_of_crates.pop())
        print("".join(letters))


if __name__ == "__main__":
    main()

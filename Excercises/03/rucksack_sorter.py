def find_wrong_item(rucksack: str):
    size = len(rucksack) // 2
    part_1 = set(rucksack[:size])
    part_2 = set(rucksack[size:])
    # set intersection finds the item in both parts
    return part_1 & part_2


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet += alphabet.upper()
    priorities = {k: v for k, v in zip(alphabet, range(1, 53))}
    total_priorities = 0
    with open("input.txt") as file:
        for line in file:
            wrong_item = find_wrong_item(line.strip()).pop()
            item_num = priorities[wrong_item]
            total_priorities += item_num
    print(total_priorities)


if __name__ == "__main__":
    main()

def find_wrong_item(rucksack: str):
    """Returns item common to first and second half of rucksack"""
    size = len(rucksack) // 2
    part_1 = set(rucksack[:size])
    part_2 = set(rucksack[size:])
    # set intersection finds the item in both parts
    return part_1 & part_2


def find_item_in_both_compartments(priorities: dict):
    """Sums priority of all the common items."""
    total_priorities = 0
    with open("Excercises/03/input.txt") as file:
        for line in file:
            wrong_item = find_wrong_item(line.strip()).pop()
            item_num = priorities[wrong_item]
            total_priorities += item_num
    print(f"part 1: {total_priorities}")


def find_item_in_3_rucksacks(priorities: dict):
    """
    Compares 3 rucksacks to find the common item
    """
    with open("Excercises/03/input.txt") as file:
        total_badge_num = 0
        while True:
            rucksack_1 = set(file.readline().strip())
            rucksack_2 = set(file.readline().strip())
            rucksack_3 = set(file.readline().strip())
            badge = rucksack_1 & rucksack_2 & rucksack_3
            # empty set -> end of file
            if len(badge) == 0:
                break
            badge_num = priorities[badge.pop()]
            total_badge_num += badge_num
    print(f"part 2: {total_badge_num}")


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet += alphabet.upper()
    priorities = {k: v for k, v in zip(alphabet, range(1, 53))}
    find_item_in_both_compartments(priorities)
    find_item_in_3_rucksacks(priorities)


if __name__ == "__main__":
    main()

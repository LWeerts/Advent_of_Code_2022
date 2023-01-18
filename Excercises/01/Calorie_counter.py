"""
Counts calories that each elf carries. Advent of code day 1

input: file with calories (int) on each line
blank line indicates end of one elf, beginning of next
"""


def main():
    with open("Excercises/01/input.txt") as file:
        calories = 0  # current counter
        calorie_list = []  # keeps track of all totals
        for line in file:
            if line == "\n":
                # new elf
                calorie_list.append(calories)
                calories = 0
                continue
            calories += int(line)
        calorie_list.append(calories)
        print(f"total of heviest elf: {max(calorie_list)}")
        calorie_list.sort(reverse=True)
        print(f"total of 3 heaviest elfs: {sum(calorie_list[0:3])}")


if __name__ == "__main__":
    main()

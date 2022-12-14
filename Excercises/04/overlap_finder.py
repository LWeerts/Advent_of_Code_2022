def main():
    count = 0
    with open("input.txt") as file:
        for line in file:
            part_1, part_2 = line.split(",")
            start_1, end_1 = part_1.split("-")
            start_2, end_2 = part_2.split("-")
            set_1 = set(range(int(start_1), int(end_1) + 1))
            set_2 = set(range(int(start_2), int(end_2) + 1))
            # check if 1 set inside other set
            if set_1 <= set_2 or set_1 >= set_2:
                count += 1
    print(f"part 1: {count}")


if __name__ == "__main__":
    main()

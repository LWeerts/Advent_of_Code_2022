

def main():
    with open("input.txt") as file:
        datastream = file.readline()
    for ix in range(0, len(datastream) - 3):
        bit = datastream[ix: ix + 14]
        if len(set(bit)) == 14:
            print(f"Found start_of_packet at index {ix + 14}")
            print(bit)
            quit()


if __name__ == "__main__":
    main()



class Comparator():
    def __init__(self, inp_1, inp_2) -> None:
        if type(inp_1) == str:
            self.inp_1 = self.parse_input(inp_1)
        else:
            self.inp_1 = inp_1
        if type(inp_2) == str:
            self.inp_2 = self.parse_input(inp_2)
        else:
            self.inp_2 = inp_2

    def parse_input(self, inp):
        output = []
        current_list = output
        parent_list = []
        for ix, char in enumerate(inp):
            if ix == 0:
                continue
            if char == "[":
                current_list.append([])
                parent_list.append(current_list)
                current_list = current_list[-1]
            elif char == "]":
                if ix + 1 == len(inp):
                    continue
                current_list = parent_list.pop()
            elif char == ",":
                continue
            elif char in "1234567890":
                if char == "1" and inp[ix + 1] == "0":
                    continue
                elif char == "0" and inp[ix - 1] == "1":
                    current_list.append(10)
                else:
                    current_list.append(int(char))
        return output

    def compare(self, inp_1, inp_2):
        ix = 0
        while True:
            try:
                item_1, item_2 = inp_1[ix], inp_2[ix]
            except IndexError:
                if len(inp_1) < len(inp_2):
                    return "L"
                elif len(inp_1) > len(inp_2):
                    return "R"
                else:
                    return "E"

            if type(item_1) == list and type(item_2) == list:
                list_compare = self.compare(item_1, item_2)

            elif type(item_1) == int and type(item_2) == int:
                if item_1 < item_2:
                    return "L"
                elif item_1 > item_2:
                    return "R"
                else:
                    ix += 1
                    continue

            elif type(item_1) == int and type(item_2) == list:
                list_compare = self.compare([item_1], item_2)

            elif type(item_1) == list and type(item_2) == int:
                list_compare = self.compare(item_1, [item_2])

            if list_compare in "RL":
                return list_compare
            elif list_compare == "E":
                ix += 1


def main_part_1():
    with open("Excercises/13/input.txt") as file:
        ix_sum = 0
        all_inputs = []
        for ix in range(1, 151):
            pass
            inp_1 = file.readline().strip()
            inp_2 = file.readline().strip()
            _ = file.readline()
            pair_comparator = Comparator(inp_1, inp_2)

            result = pair_comparator.compare(
                pair_comparator.inp_1, pair_comparator.inp_2)
            if result == "L":
                ix_sum += ix
            elif result == "E":
                print(f"A pair is identical, at index {ix}")
            all_inputs.append(pair_comparator.inp_1)
            all_inputs.append(pair_comparator.inp_2)

    print(f"The sum of indexes is {ix_sum}")
    return all_inputs


def main_part_2(all_inputs):
    all_inputs.append([[2]])
    all_inputs.append([[6]])
    sorted_output = []
    for inp in all_inputs:
        low_bound = 0
        high_bound = len(sorted_output)
        while low_bound != high_bound:
            target = (low_bound + high_bound) // 2
            comp = Comparator(inp, sorted_output[target])
            left_right = comp.compare(comp.inp_1, comp.inp_2)
            if left_right == "L":
                high_bound = target
            elif left_right == "R":
                low_bound = target + 1
            else:
                print(f"Comparison failed at input {inp}")
                quit()
        else:
            sorted_output.insert(low_bound, inp)
    packet_1 = sorted_output.index([[2]]) + 1
    packet_2 = sorted_output.index([[6]]) + 1
    decoder_key = packet_1 * packet_2
    print(decoder_key)


def main():
    all_inputs = main_part_1()
    main_part_2(all_inputs)


if __name__ == "__main__":
    main()

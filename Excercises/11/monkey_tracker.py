class Monkey():
    """Inspects items and throws it to other monkeys"""

    def __init__(self, throwables, operation, div_by,
                 true_target, false_target) -> None:
        self.throwables = [int(x) for x in throwables]
        self.parse_operation(operation)
        self.div_by = int(div_by)
        self.true_target_num = int(true_target)
        self.false_target_num = int(false_target)
        self.num_inspected = 0

    def parse_operation(self, operation: str):
        self.op_type = operation.split()[-2]
        self.op_arg = operation.split()[-1]

    def aquire_targets(self, monkey_list):
        self.true_target = monkey_list[self.true_target_num].throwables
        self.false_target = monkey_list[self.false_target_num].throwables

    def op_function(self, input_1: int, op_type, input_2):
        if input_2 == "old":
            input_2 = input_1
        else:
            input_2 = int(input_2)
        if op_type == "+":
            return input_1 + input_2
        elif op_type == "*":
            return input_1 * input_2

    def div_and_round(self, num: int) -> int:
        return num % 9699690
        # return num

    def my_turn(self):
        for item in self.throwables:
            new_num = self.op_function(item, self.op_type, self.op_arg)
            new_num = self.div_and_round(new_num)
            if new_num % self.div_by == 0:
                self.true_target.append(new_num)
            else:
                self.false_target.append(new_num)
            self.num_inspected += 1
        self.throwables.clear()


def main():
    monkey_list = []
    with open("Excercises/11/input.txt") as file:
        for line in file:
            if line.startswith("Monkey"):
                starting_items = file.readline().split(":")[-1].split(",")
                operation = file.readline()
                div_by = file.readline().split()[-1]
                true_target = file.readline().split()[-1]
                false_target = file.readline().split()[-1]
                monkey_list.append(Monkey(
                    starting_items, operation, div_by,
                    true_target, false_target
                ))
        for monkey in monkey_list:
            monkey.aquire_targets(monkey_list)
    for turn in range(10000):

        print(turn)
        for monkey in monkey_list:
            monkey.my_turn()
        # for ix, monkey in enumerate(monkey_list):
            # print(f"Monkey {ix}: {monkey.throwables}")
    inspected_list = []
    for monkey in monkey_list:
        inspected_list.append(monkey.num_inspected)
    inspected_list.sort()  # Ascending order
    print(inspected_list[-1] * inspected_list[-2])


if __name__ == "__main__":
    main()

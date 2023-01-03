class Movable():
    """Can move on a square grid"""

    def __init__(self) -> None:
        self.x_coord = 0
        self.y_coord = 0

    def move(self, direction: str) -> None:
        for letter in direction:
            if letter == "L":
                self.x_coord -= 1
            if letter == "R":
                self.x_coord += 1
            if letter == "U":
                self.y_coord += 1
            if letter == "D":
                self.y_coord -= 1

    def pos(self) -> tuple[int]:
        return (self.x_coord, self.y_coord)


class Head(Movable):
    """Moves according to the input instructions"""


class Tail(Movable):
    """Moves to follow the Head"""

    def __init__(self) -> None:
        super().__init__()
        self.visited_pos = set()
        self.visited_pos.add((0, 0))
        self.move_count = 0

    def follow_Head(self, target: Head) -> None:
        """Determines if and which step needs to be taken"""
        delta_x = target.pos()[0] - self.pos()[0]
        delta_y = target.pos()[1] - self.pos()[1]

        instruction = ""
        if delta_x == 2:
            instruction += "R"
        elif delta_x == -2:
            instruction += "L"
        if delta_y == 2:
            instruction += "U"
        elif delta_y == -2:
            instruction += "D"
        # If we move, prefer to move diagonally
        # instruction must not be empty
        if instruction and instruction in "RL":
            if delta_y == 1:
                instruction += "U"
            elif delta_y == -1:
                instruction += "D"
        if instruction and instruction in "UD":
            if delta_x == 1:
                instruction += "R"
            elif delta_x == -1:
                instruction += "L"
        self.move(instruction)
        self.visited_pos.add(self.pos())

    def count_visited_pos(self):
        return len(self.visited_pos)


def main_part_1():
    """Rope of length 2"""
    front = Head()
    back = Tail()
    with open("Excercises/09/input.txt") as file:
        for line in file:
            if line == "":
                continue
            direction, amount = line.split()
            amount = int(amount)
            for _ in range(amount):
                front.move(direction)
                back.follow_Head(front)
    print(back.count_visited_pos())


def main_part_2():
    """Rope of lenght 10"""
    rope = []
    rope.append(Head())
    for _ in range(9):
        rope.append(Tail())
    with open("Excercises/09/input.txt") as file:
        for line in file:
            if line == "":
                continue
            direction, amount = line.split()
            amount = int(amount)
            for _ in range(amount):
                rope[0].move(direction)  # Move the head
                for ix in range(9):
                    # Move each tail sequentially
                    rope[ix + 1].follow_Head(rope[ix])
    # Answer is positions visited by the rear of the rope
    print(rope[-1].count_visited_pos())


def main():
    main_part_1()
    main_part_2()


if __name__ == "__main__":
    main()

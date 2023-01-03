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
        # self.visited_pos = []
        # self.visited_pos.append((0, 0))
        print(self.visited_pos)
        self.move_count = 0

    def follow_Head(self, target: Head) -> None:
        delta_x = target.pos()[0] - self.pos()[0]
        delta_y = target.pos()[1] - self.pos()[1]

        instruction = ""
        if delta_x > 1:
            instruction += "R"
        elif delta_x < -1:
            instruction += "L"
        if delta_y > 1:
            instruction += "U"
        elif delta_y < -1:
            instruction += "D"
        if instruction:
            self.move_count += 1
        # If we move, prefer to move diagonally
        if instruction in "RL":
            if delta_y > 0:
                instruction += "U"
            elif delta_y < 0:
                instruction += "D"
        if instruction in "UD":
            if delta_x > 0:
                instruction += "R"
            elif delta_x < 0:
                instruction += "L"
        # print(delta_x, delta_y, instruction)
        self.move(instruction)
        self.visited_pos.add(self.pos())
        # self.visited_pos.append(self.pos())

    def count_visited_pos(self):
        return len(self.visited_pos)


def main():
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
                # print(back.pos())
    print(back.count_visited_pos())
    # print(back.move_count)
    # print(back.visited_pos)


if __name__ == "__main__":
    main()

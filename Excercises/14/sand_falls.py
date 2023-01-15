import numpy as np


class PlayingField():
    """Handles reading the scan-map"""
    def __init__(self, part_1_2) -> None:
        # Initialize an empty field, y coord of 200 is top down!
        self.field = np.full((200, 1000), " ", dtype="U1")
        self.highest_y = self.read_map()
        if part_1_2 == 1:
            # Part 1: Bottom row is abyss
            self.field[-1, :][self.field[-1, :] == " "] = "A"
        elif part_1_2 == 2:
            # Part 2: 2 below lowest rock is cave floor
            self.field[self.highest_y + 2, :] = "#"

    def read_map(self):
        """Reads the input, converts rock locations and populates the map"""
        highest_y = 0
        with open("Excercises/14/input.txt") as file:
            for line in file:
                split_line = line.split(" -> ")
                point_list = []
                for point in split_line:
                    coord_x, coord_y = point.split(",")
                    # Flip coordinates so it matches numpy array indices
                    point_list.append((int(coord_y), int(coord_x)))
                    if int(coord_y) > highest_y:
                        highest_y = int(coord_y)  # For part 2
                for pair in zip(point_list[:-1], point_list[1:]):
                    min_y, max_y = sorted((pair[0][0], pair[1][0]))
                    min_x, max_x = sorted((pair[0][1], pair[1][1]))
                    # Exclusive stop -> max_y + 1
                    self.field[min_y: max_y + 1, min_x: max_x + 1] = "#"
        return highest_y


class Sand():
    """Handles flooding of cave with sand"""
    def __init__(self, playing_field) -> None:
        self.field = playing_field.field

    def next_move(self, coord_y, coord_x):
        """Determines next possible move and returns coordinates.

        Sand moves down, or down-left, or down-right, or rests.

        Returns (x, y) if sand can fall to that coordinate
        Returns ('Rest', y, x) if sand rests
        Returns ('End', y, x) if sand reaches abyss
        """
        if self.field[coord_y + 1, coord_x] == " ":
            return coord_y + 1, coord_x
        elif self.field[coord_y + 1, coord_x - 1] == " ":
            return coord_y + 1, coord_x - 1
        elif self.field[coord_y + 1, coord_x + 1] == " ":
            return coord_y + 1, coord_x + 1
        elif np.any(self.field[coord_y + 1, coord_x - 1:coord_x + 2] == "A"):
            # Sand can fall into the abyss, so simulation complete
            return ("End", coord_y, coord_x)
        else:
            return ("Rest", coord_y, coord_x)

    def drop_sand(self):
        """Fills cave with sand"""
        drop_result = (0, 500)  # Spawn location
        while drop_result[0] != "End":
            drop_result = (0, 500)
            # If sand reaches spawn point, no more sand spawns
            if self.field[0, 500] == "o":
                break
            while drop_result[0] != "Rest":
                # Move to the next position
                drop_result = self.next_move(*drop_result)
                if drop_result[0] == "End":
                    break
            else:  # Only if sand should rest
                self.field[drop_result[1], drop_result[2]] = "o"

    def num_of_sand(self):
        return np.count_nonzero(self.field == "o")


def main():
    field = PlayingField(2)  # Enter 1 or 2 for part 1 or 2
    # print(field.field[:12, 493:505])  # Check the input_test.txt field
    sandfall = Sand(field)
    sandfall.drop_sand()
    print(sandfall.num_of_sand())


if __name__ == "__main__":
    main()
"""Advent of Code exercise 14.

This module is my solution to the 14th problem of the Advent of Code
2022. The problem can be found at https://adventofcode.com/2022/day/14.

Exercise summary:
    The input consists of coordinates of straight lines of rock. The
    cave that the rock makes up, will be filled with blocks of sand
    falling one by one. The sand spawns at 500, 0 and falls down, or
    down and left, or down and right, otherwise it comes to rest.

    Part 1:
    Count how many blocks of sand come to rest before sand starts
    falling into the abyss below the cave?

    Part 2:
    The cave now has a floor, 2 layers lower than the lowest block of
    rock, and infinitely wide. How many blocks of sand can spawn until
    the spawnpoint is blocked by sand?

Author: Luc Weerts
Date: Jan 13, 2023
"""


import numpy as np


class PlayingField():
    """Handles reading the scan-map.
    
    Args:
        part_1_2 (int): If 1, row 1000 of the cave is set to 'A' for 
            abyss. If 2, the cave floor is generated 2 layers below the
            lowest rock.
    
    Attributes:
        field (numpy.NDarray): 200 by 1000 array containing single
            letters. ' ' is empty space, '#' is rock, 'A' is abyss and
            'o' is sand. 
        
    """
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
        """Reads the input, converts rock locations and populates the map.
        
        Returns:
            int: The highest y coordinate of rock.
        """
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
    """Handles flooding of cave with sand.
    
    Args:
        field (numpy.NDarray): Field with rock, to be filled with sand.
    
    Attributes:
        field (numpy.NDarray): Field with rock, to be filled with sand.
    """
    def __init__(self, field) -> None:
        self.field = field

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
        """Fills cave with sand.
        
        Modifies self.field to fill the cave with sand.
        Calls self.next_move until sand comes to rest.
        """
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
    sandfall = Sand(field.field)
    sandfall.drop_sand()
    print(sandfall.num_of_sand())


if __name__ == "__main__":
    main()

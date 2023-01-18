"""Advent of code exercise 12.

This module is my solution to the 12th problem of the Advent of Code
2022. The problem can be found at https://adventofcode.com/2022/day/12.

Exercise summary:
    The exercise requires pathfinding over a 41 by 78 grid (row,
    column). The grid has altitude indicated by lowercase letters, with
    start and end indicated with capital S and E. Steps are only allowed
    up, down, left or right, and if the target location is at most 1
    elevation higher than the current location.

    Part 1:
    Find the length of the shortest path between start and end.

    Part 2:
    Find the location with elevation 0 with the shortest path to the
    end.

To Do:
    * input_test.txt -> certain output
    * more comments???
    * restructure to sourcefiles and datafiles
    * add __init__.py and a main executable that calls other scripts
    * requirements.txt
    * pathlib


Author: Luc Weerts
Date: Jan 7, 2023
"""


import numpy as np


class Hero():
    """Enables pathfinding on the map.

    Args:
        chart (numpy.ndarray): heightmap, navigated by the Hero
        letter_chart (numpy.ndarray): unparsed chart, used for setting
            start and finish locations

    Attributes:
        visited (numpy.ndarray): each int represents how far away from
            the start this location is. Unmapped = -1
        pathlength (int): pathlength to farthest explored tile
    """

    def __init__(self, chart, letter_chart):
        self.__chart = chart
        self.__letter_chart = letter_chart
        self.visited = np.zeros(self.__chart.shape, dtype=np.int32) - 1
        self.__pos_x, self.__pos_y = np.nonzero(self.__letter_chart == "S")
        self.visited[self.__pos_x, self.__pos_y] = 0  # Start location
        end = np.nonzero(self.__letter_chart == "E")
        self.__finish_x, self.__finish_y = end
        self.pathlength = 0

    def alt(self, pos_x, pos_y):
        """For getting the altitude at the target location

        Args:
            pos_x (int): x coordinate
            pos_y (int): y coordinate

        Returns:
            int: altitude
        """
        return self.__chart[pos_x, pos_y]

    def check_finished(self):
        """Check if the finish is visited, thus we are done.

        Returns:
            bool: True if finished else False
        """
        return self.visited[self.__finish_x, self.__finish_y] != -1

    def identify_moves(self, pos_x, pos_y):
        """Checks possible moves and, if allowed, adds them to visited.

        The four cardinal directions are checked. If they are not
        already visited, and the elevation is at most 1 greater than
        current elevation, then that direction is marked in visited
        with the pathlength to that point.

        Args:
            pos_x (int): x coordinate
            pos_y (int): y coordinate

        Returns:
            None
        """
        for direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            new_x = pos_x + direction[0]
            new_y = pos_y + direction[1]
            # Don't want to check negative coordinate, it is other side of map
            if new_x < 0 or new_y < 0:
                continue
            try:
                if (
                    self.visited[new_x, new_y] == -1
                    and
                    self.alt(pos_x, pos_y) + 1 >= self.alt(new_x, new_y)
                ):
                    self.visited[new_x, new_y] = self.pathlength + 1
            except IndexError:
                continue


class ShortestPathFinder(Hero):
    """Modified Hero to allow any starting location.

    Args:
        chart (numpy.ndarray): heightmap, navigated by the Hero
        letter_chart (numpy.ndarray): unparsed chart, used for setting
            start and finish locations
        pos_x (int): starting x coordinate
        pos_y (int): starting y coordinate

    Attributes:
        visited (numpy.ndarray): each int represents how far away from
            the start this location is. Unmapped = -1
        pathlength (int): pathlength to farthest explored tile
    """
    def __init__(self, chart, letter_chart, pos_x, pos_y) -> None:
        super().__init__(chart, letter_chart)
        self.__pos_x, self.__pos_y = pos_x, pos_y
        self.visited[self.__pos_x, self.__pos_y] = 0  # Start location


def chart_reader(input_file):
    """Parses and converts the map.

    returns chart (with numbers for altitude)
            and letter_chart (for finding start and end location)
    """
    letter_chart = np.genfromtxt(input_file, delimiter=1, dtype="U1")
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    convert_dict = {"S": 0, "E": 25}
    for num, letter in enumerate(alphabet):
        convert_dict[letter] = num
    chart = [convert_dict[letter] for letter in letter_chart.ravel()]
    chart = np.array(chart).reshape(letter_chart.shape)
    return chart, letter_chart


def find_shortest_path(input_file):
    """Determines length of the shortest path.

    Iterates over locations reachable by the explorer in pathlength
    steps, then increases pathlength. explorer.identify_moves() updates
    explorer.visited.
    """
    chart, letter_chart = chart_reader(input_file)
    explorer = Hero(chart, letter_chart)
    while not explorer.check_finished():
        # Grab all locations we found in the previous iteration
        coords = np.nonzero(explorer.visited == explorer.pathlength)
        for px, py in zip(coords[0], coords[1]):
            explorer.identify_moves(px, py)
        explorer.pathlength += 1
    print(explorer.pathlength)


def find_closest_start(input_file):
    """Determines shortest path of the closest starting position.

    Iterates over all starting positions of elevation 0, and prints the
    shortest pathlength that was found.

    """
    chart, letter_chart = chart_reader(input_file)
    # Find all starting locations to loop through
    starting_locs = np.argwhere(chart == 0)
    shortest_path_length = 9999999999999999
    paths_explored = 0

    for start_x, start_y in starting_locs:
        if paths_explored % 10 == 0:
            print(f"paths_explored {paths_explored}")  # To see progress

        scout = ShortestPathFinder(chart, letter_chart, start_x, start_y)
        while not scout.check_finished():
            coords = np.nonzero(scout.visited == scout.pathlength)
            if len(coords[0]) == 0:  # Stuck with no path to the finish
                paths_explored += 1
                break
            for px, py in zip(coords[0], coords[1]):
                scout.identify_moves(px, py)
            scout.pathlength += 1

        else:  # Only execute if finish is reached
            paths_explored += 1
            if scout.pathlength < shortest_path_length:
                shortest_path_length = scout.pathlength
    print(f"shortest path length {shortest_path_length}")


def main():
    input_file = "Excercises/12/input.txt"
    find_shortest_path(input_file)
    find_closest_start(input_file)


if __name__ == "__main__":
    main()

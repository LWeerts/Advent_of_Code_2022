"""Advent of code excercise 12.

This module is my solution to the 12th problem of the Advent of Code
2022. The problem can be found at https://adventofcode.com/2022/day/12.

Excercise summary:
    The excercise requires pathfinding over a 41 by 78 grid (row,
    column). The grid has altitude indicated by lowercase letters, with
    start and end indicated with capital S and E.

To Do:
    * super.__init__ for ShortestPathFinder
    * Internalize Hero attributes
    * Write docstrings (https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
    * Check all docstrings
    * del scout
    * input_test.txt -> certain output
    * more comments???
    * replace numpy.nonzero with the per-item grouped one
    * restructure to sourcefiles and datafiles
    * add __init__.py and a main executable that calls other scripts
    * check pep8 compliance
    * requirements.txt
    * pathlib



Author: Luc Weerts
Date: Jan 7, 2023
"""


import numpy as np


class Hero():
    """Can move on the map.
    
    Attributes:
        chart (numpy.ndarray): heightmap, navigated by the Hero.
        visited (numpy.ndarray): each int represents how far away from
            the start this location is. Unmapped = -1
        pathlength (int): pathlength to farthest explored tile
    """

    def __init__(self, chart, letter_chart) -> None:
        self.__chart = chart
        self.__letter_chart = letter_chart
        self.visited = np.zeros(self.__chart.shape, dtype=np.int32) - 1
        self.__pos_x, self.__pos_y = np.nonzero(self.__letter_chart == "S")
        self.visited[self.__pos_x, self.__pos_y] = 0  # Start location
        self.__finish_x, self.__finish_y = np.nonzero(self.__letter_chart == "E")
        self.pathlength = 0

    def alt(self, pos_x, pos_y):
        """For getting the altitude at the target location"""
        return self.__chart[pos_x, pos_y]

    def check_finished(self):
        """Check if the finish is visited, thus we are done"""
        return self.visited[self.__finish_x, self.__finish_y] != -1

    def identify_moves(self, pos_x, pos_y):
        """
        Check all 4 directions for if moving is possible
        and adds them to the visited chart.
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
                    self.alt(pos_x, pos_y) + 1 >= self.__chart[new_x, new_y]
                ):
                    self.visited[new_x, new_y] = self.pathlength + 1
            except IndexError:
                continue


class ShortestPathFinder(Hero):
    """Modified Hero to allow any starting location"""
    def __init__(self, chart, letter_chart, pos_x, pos_y) -> None:
        super().__init__(chart, letter_chart)
        self.__pos_x, self.__pos_y = pos_x, pos_y
        self.visited[self.__pos_x, self.__pos_y] = 0  # Start location


def chart_reader():
    """
    Parses and converts the map.

    returns chart (with numbers for altitude)
            and letter_chart (for finding start and end location)
    """
    letter_chart = np.genfromtxt("Excercises/12/input.txt",
                                 delimiter=1, dtype="U1")
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    convert_dict = {"S": 0, "E": 25}
    for num, letter in enumerate(alphabet):
        convert_dict[letter] = num
    chart = [convert_dict[letter] for letter in letter_chart.ravel()]
    chart = np.array(chart).reshape(letter_chart.shape)
    return chart, letter_chart


def main_part_1():
    chart, letter_chart = chart_reader()
    explorer = Hero(chart, letter_chart)
    while not explorer.check_finished():
        # Grab all locations we found in the previous iterartion
        coords = np.nonzero(explorer.visited == explorer.pathlength)
        for px, py in zip(coords[0], coords[1]):
            explorer.identify_moves(px, py)
        explorer.pathlength += 1
    print(explorer.pathlength)


def main_part_2():
    chart, letter_chart = chart_reader()
    # Find all starting locations to loop through
    starting_locs = np.nonzero(chart == 0)
    shortest_path_length = 9999999999999999
    paths_explored = 0

    for start_x, start_y in zip(starting_locs[0], starting_locs[1]):
        print(f"paths_explored {paths_explored}")  # To see progress
        scout = ShortestPathFinder(chart, letter_chart, start_x, start_y)
        while not scout.check_finished():
            coords = np.nonzero(scout.visited == scout.pathlength)
            if len(coords[0]) == 0:  # Stuck with no path to the finish
                paths_explored += 1
                del scout
                break
            for px, py in zip(coords[0], coords[1]):
                scout.identify_moves(px, py)
            scout.pathlength += 1

        else:  # Only execute if finish is reached
            paths_explored += 1
            if scout.pathlength < shortest_path_length:
                shortest_path_length = scout.pathlength
            del scout
    print(f"shortest path length {shortest_path_length}")


def main():
    main_part_1()
    main_part_2()


if __name__ == "__main__":
    main()

import numpy as np


class Hero():
    """Can move on the map"""

    def __init__(self, chart, letter_chart) -> None:
        self.chart = chart
        self.letter_chart = letter_chart
        self.visited = np.zeros(self.chart.shape, dtype=np.int32) - 1
        self.pos_x, self.pos_y = np.nonzero(self.letter_chart == "S")
        self.visited[self.pos_x, self.pos_y] = 0  # Start location
        self.finish_x, self.finish_y = np.nonzero(self.letter_chart == "E")
        self.pathlength = 0

    def alt(self, pos_x, pos_y):
        """For getting the altitude at the target location"""
        return self.chart[pos_x, pos_y]

    def check_finished(self):
        """Check if the finish is visited, thus we are done"""
        return self.visited[self.finish_x, self.finish_y] != -1

    def identify_moves(self, pos_x, pos_y):
        """
            Check all 4 directions for if moving is possible
            and adds them to the visited chart.
        """
        for direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            new_x = pos_x + direction[0]
            new_y = pos_y + direction[1]
            # Don't want to check -1 coordinate, it is other side of map
            if new_x < 0 or new_y < 0:
                continue
            try:
                if (self.visited[new_x, new_y] == -1
                        and self.alt(pos_x, pos_y) + 1
                        >= self.chart[new_x, new_y]):
                    self.visited[new_x, new_y] = self.pathlength + 1
            except IndexError:
                continue


class ShortestPathFinder(Hero):
    """Modified Hero to allow any starting location"""
    def __init__(self, chart, letter_chart, pos_x, pos_y) -> None:
        self.chart = chart
        self.letter_chart = letter_chart
        self.visited = np.zeros(self.chart.shape, dtype=np.int32) - 1
        self.pos_x, self.pos_y = pos_x, pos_y
        self.visited[self.pos_x, self.pos_y] = 0  # Start location
        self.finish_x, self.finish_y = np.nonzero(self.letter_chart == "E")
        self.pathlength = 0


def chart_reader():
    """
    Func to parse and convert the map.

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

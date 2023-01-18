"""Advent of code exercise 15.

This module is my solution to the 15th problem of the Advent of Code
2022. The problem can be found at https://adventofcode.com/2022/day/15.

Exercise summary:
    The exercise gives sensor locations, each having the location of
    the nearest beacon attached. Distance is calculated as Manhattan
    distance throughout the exercise. Since each sensor reports the
    nearest beacon, an area around the sensor cannot contain other
    beacons. However, the distress beacon that must be found is not
    reported by the sensors, so the goal is to find the beacon by
    eliminating all locations where it cannot be.

    Part 1:
    Count all positions in row y=2_000_000 that are blocked by sensor
    range.

    Part 2:
    Consider the area 0 to 4_000_000 (inclusive) in x and y. Find the
    single position that is not in sensor range.

To Do
    * Clean up main() (segment to more functions)
    * Main executable handles input.txt?
    * input.txt vs Excercises/xx/input.txt
    * Convert different strats of part 2 to separate functions
    * pref_block -> pref_block

Author: Luc Weerts
Date: Jan 7, 2023
"""


import numpy as np


class Sensor():
    """Stores own and beacon location, can calculate blockage on line.

    Args:
        coord_x (int): Own x coordinate.
        coord_y (int): Own y coordinate.
        beacon_x (int): Beacon x coordinate.
        beacon_y (int): Beacon y coordinate.

    Attributes:
        coord_x (int): Own x coordinate.
        coord_y (int): Own y coordinate.
        beacon_x (int): Beacon x coordinate.
        beacon_y (int): Beacon y coordinate.
        man_dist (int): Manhattan distance between sensor and beacon.
    """
    def __init__(self, coord_x, coord_y, beacon_x, beacon_y):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y
        self.man_dist = manhattan_dist(coord_x, coord_y, beacon_x, beacon_y)

    def block_on_line(self, line):
        """Returns range of blockage on target line.

        Args:
        line (int): Target line to check.

        Returns:
            None: If sensor does not block target line.
            list: [start, end] otherwise (end is exclusive).
        """
        delta_y = abs(self.coord_y - line)
        surplus = self.man_dist - delta_y
        if surplus < 0:
            return None
        return [self.coord_x - surplus, self.coord_x + 1 + surplus]


def manhattan_dist(x1, y1, x2, y2):
    """Calculates the Manhattan distance between 2 points

    Args:
        x1 (int): x coordinate of point 1.
        y1 (int): y coordinate of point 1.
        x2 (int): x coordinate of point 2.
        y2 (int): y coordinate of point 2.

    Returns:
        int: Manhattan distance.
    """
    return abs(x1 - x2) + abs(y1 - y2)


def parse_input(input_file):
    """Reads input, returns sensor list sorted by x coordinate.

    Args:
        input_file (str): Location of input file, relative to working
            dir.

    Returns:
        list: Contains Sensor objects, sorted by Sensor x coordinate.
    """
    sensor_list = []
    with open(input_file) as file:
        for line in file:
            split_line = line.split()
            coord_x = int(split_line[2].strip("xy=,:"))
            coord_y = int(split_line[3].strip("xy=,:"))
            beacon_x = int(split_line[8].strip("xy=,:"))
            beacon_y = int(split_line[9].strip("xy=,:"))
            sensor_list.append(Sensor(coord_x, coord_y, beacon_x, beacon_y))

    sensor_list.sort(key=lambda sensor: sensor.coord_x)
    return sensor_list


def find_all_blocked_on_line(sensor_list, line):
    """Finds the number of blocked locations on a line.

    Uses a set to contain ints representing x coordinates. Ranges of
    ints are added to the set for each sensor. Beacon locations must
    be removed as they are not blocked, but occupied.

    Args:
        sensor_list (list): Contains Sensor objects, sorted by
            Sensor x coordinate.
    """

    blocked_locations = set()
    for sensor in sensor_list:
        block = sensor.block_on_line(line)
        if block is None:
            continue
        # Fill set with integers for all blocked x coordinates
        blocked_locations.update(range(*block))

    for sensor in sensor_list:
        if sensor.beacon_y == line:
            # Remove beacons themselves
            blocked_locations.discard(sensor.beacon_x)

    print(len(blocked_locations))


def find_non_blocked_1(sensor_list):
    """Find possible beacon location, very slowly.

    Adds ranges of integers to a set. If set is shorter than 4_000_000,
    then there is a possible beacon location.
    This implementation is very slow, ~ 10 lines/s, so this is not
    actually used. It has to store 4 million ints during each iteration.

    Args:
        sensor_list (list): Contains Sensor objects, sorted by
            Sensor x coordinate.
    """

    blocked_locations = set()
    range_x = set(range(0, 4_000_001))
    for line in range(0, 4_000_001):
        if line % 10 == 0:
            print(line)
        for sensor in sensor_list:
            blocked_locations.update(range(*sensor.block_on_line(line)))
        if len(blocked_locations) < 4_000_000:
            coord_x = blocked_locations.difference(range_x)
            print(f"found possible beacon location at {coord_x}, {line}")


def find_non_blocked_2(sensor_list):
    """Find possible beacon location, slowly.

    Uses a numpy array to keep track of which positions are blocked.
    True = blocked, False = open
    Slow, ~ 200 lines/s. Stores 4 million bools instead of ints.

    Args:
        sensor_list (list): Contains Sensor objects, sorted by
            Sensor x coordinate.
    """

    blocked_locations = np.zeros(4_000_001, dtype=bool)
    for line in range(0, 4_000_001):
        if line % 1000 == 0:
            print(line)
        blocked_locations[:] = False  # Reset array

        for ix, sensor in enumerate(sensor_list):
            block = sensor.block_on_line(line)
            if block is None:
                continue
            # Avoid overflow
            if block[0] < 0:
                block[0] = 0
            if block[1] > 4_000_001:
                block[1] = 4_000_001
            blocked_locations[block[0]: block[1]] = True

        if np.any(blocked_locations == False):
            print(np.nonzero(blocked_locations == False)[0], line)


def merge_blocks(block, blocked_locations):
    """Fuses start and stop of block with blocks in blocked_locations.

    Args:
        block (list): Start and stop of the current sensor block range.
        blocked_locations (list): Contains blocks of start and stop from
            the previous sensors.

    Returns:
        list: blocked_locations with overlapping ranges merged.
    """
    new_blocked_locations = []
    for pref_block in blocked_locations:
        if (
            pref_block[0] <= block[0] <= pref_block[1]
            or block[0] <= pref_block[0] <= block[1]
        ):
            # block and pref_block overlap, so fuse together
            block = [
                min(pref_block[0], block[0]),
                max(pref_block[1], block[1])
            ]
        else:
            # Store pref_block for next sensor
            new_blocked_locations.append(pref_block)
    new_blocked_locations.append(block)
    return new_blocked_locations


def find_non_blocked_3(sensor_list):
    """Find possible beacon location, quickly.

    Keeps track of start and end of blocked ranges.
    Merges new blocked range with old range if they overlap.
    Much faster than the other implementations, over 100_000 lines/s.

    Args:
        sensor_list (list): Contains Sensor objects, sorted by
            Sensor x coordinate.
    """

    for line in range(0, 4_000_001):
        if line % 100_000 == 0:
            print(line)  # Visualize progress
        blocked_locations = []
        for sensor in sensor_list:
            block = sensor.block_on_line(line)
            if block is None:  # Not blocking this line so skip
                continue
            if not blocked_locations:  # List still empty
                blocked_locations.append(block)
                continue

            # Merge block with previous blocks
            blocked_locations = merge_blocks(block, blocked_locations)
        if len(blocked_locations) != 1:
            print(blocked_locations[0][1] * 4000000 + line)


def main():
    input_file = "Excercises/15/input.txt"
    sensor_list = parse_input(input_file)
    line = 2_000_000
    find_all_blocked_on_line(sensor_list, line)
    find_non_blocked_3(sensor_list)


if __name__ == "__main__":
    main()

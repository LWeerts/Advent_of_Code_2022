"""


To Do
    * Clean up main() (segment to more functions)
    * Main executable handles input.txt?
    * input.txt vs Excercises/xx/input.txt
    * Convert different strats of part 2 to separate functions
    * loc -> pref_block
"""


import numpy as np


class Sensor():
    def __init__(self, coord_x, coord_y, beacon_x, beacon_y) -> None:
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y
        self.man_dist = manhattan_dist(coord_x, coord_y, beacon_x, beacon_y)

    def block_on_line(self, line):
        """Returns range of blockage on target line.

        input:
        line = int

        output:
        None (if this sensor does not block the target line
        [start, end] (if blocking the line, end is inclusive)
        """
        delta_y = abs(self.coord_y - line)
        surplus = self.man_dist - delta_y
        if surplus < 0:
            return None
        return [self.coord_x - surplus, self.coord_x + 1 + surplus]


def manhattan_dist(x1, y1, x2, y2):
    """Return the Manhattan distance between 2 points"""
    return abs(x1 - x2) + abs(y1 - y2)


def parse_input():
    """Reads input, returns sensor list sorted by x coordinate"""
    sensor_list = []
    with open("Excercises/15/input.txt") as file:
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
    # Part 1
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
    actually used.
    """

    blocked_locations = set()
    range_x = set(range(0, 4_000_001))
    for line in range(0, 4_000_001):
        if line % 10 == 0:
            print(line)
        for sensor in sensor_list:
            blocked_locations.update(range(*sensor.block_on_line(line)))
        if len(blocked_locations) < 4_000_000:
            coord_x = blocked_locations.difference(range(0, 4_000_001))
            print(f"found possible beacon location at {coord_x}, {line}")


def find_non_blocked_2(sensor_list):
    """Find possible beacon location, slowly.

    Uses a numpy array to keep track of which positions are blocked.
    True = blocked, False = open
    Slow, ~ 200 lines/s. Stores 4 million bools instead of ints
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


def find_non_blocked_3(sensor_list):
    """Find possible beacon location, quickly.
    
    Keeps track of start and end of blocked ranges.
    Merges new blocked range with old range if they overlap.
    Much faster than the other implementations, over 100_000 lines/s.
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
            new_blocked_locations = []
            for loc in blocked_locations:
                if (loc[0] <= block[0] <= loc[1]
                        or block[0] <= loc[0] <= block[1]):
                    # block and loc overlap, so fuse together
                    block = [min(loc[0], block[0]), max(loc[1], block[1])]
                else:
                    # Store loc for next sensor
                    new_blocked_locations.append(loc)
            new_blocked_locations.append(block)
            blocked_locations = new_blocked_locations[:]  # Copy!
        if len(blocked_locations) != 1:
            print(blocked_locations[0][1] * 4000000 + line)


def main():
    sensor_list = parse_input()
    line = 2000000
    find_all_blocked_on_line(sensor_list, line)


if __name__ == "__main__":
    main()

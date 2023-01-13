
class Sensor():
    def __init__(self, coord_x, coord_y, beacon_x, beacon_y) -> None:
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y
        self.man_dist = manhatten_dist(coord_x, coord_y, beacon_x, beacon_y)

    def block_on_line(self, line):
        delta_y = abs(self.coord_y - line)
        surplus = self.man_dist - delta_y
        return self.coord_x - surplus, self.coord_x + 1 + surplus


def manhatten_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def parse_input():
    sensor_list = []
    with open("Excercises/15/input.txt") as file:
        for line in file:
            split_line = line.split()
            coord_x = int(split_line[2].strip("xy=,:"))
            coord_y = int(split_line[3].strip("xy=,:"))
            beacon_x = int(split_line[8].strip("xy=,:"))
            beacon_y = int(split_line[9].strip("xy=,:"))
            sensor_list.append(Sensor(coord_x, coord_y, beacon_x, beacon_y))
    return sensor_list


def main():
    sensor_list = parse_input()
    line = 2000000
    blocked_locations = set()
    for sensor in sensor_list:
        blocked_locations.update(range(*sensor.block_on_line(line)))
    for sensor in sensor_list:
        if sensor.beacon_y == line:
            blocked_locations.discard(sensor.beacon_x)
    print(len(blocked_locations))
    # print(blocked_locations)


if __name__ == "__main__":
    main()

# 3559 too low, because squares at the edge of the scan are
# not counted correctly, increasing all coordinates by 1 fixes this.


import numpy as np


def read_input(filename):
    """Creates a numpy array representing the droplet"""
    with open(filename) as file:
        scan_result = np.zeros((25, 25, 25), dtype=np.int32)
        for line in file:
            if len(line) == 0:
                continue
            # Each value 1 in the array is 1 subcube of the droplet
            coords = [int(num) + 1 for num in line.split(",")]
            scan_result[coords[0], coords[1], coords[2]] = 1
    return scan_result


def calculate_surface_simple(scan_result):
    diff_x = abs(np.diff(scan_result, axis=0))
    diff_y = abs(np.diff(scan_result, axis=1))
    diff_z = abs(np.diff(scan_result, axis=2))
    surface = np.sum(diff_x) + np.sum(diff_y) + np.sum(diff_z)
    print(surface)
    return surface


def main():
    scan_result = read_input("Excercises/18/input.txt")
    surface_area = calculate_surface_simple(scan_result)


if __name__ == "__main__":
    main()

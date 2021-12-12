import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint
from scipy.ndimage.morphology import binary_erosion as erode
from scipy.ndimage.morphology import binary_dilation as dilate
from scipy.ndimage.morphology import binary_opening as open
from scipy.ndimage.morphology import binary_closing as close


def calculate_risk(sea_floor):
    # Track if a point is a minimum.
    is_minimum = np.zeros_like(sea_floor, dtype=np.bool)

    # These are the direct neighbours of a given point.
    neighbours = np.array([[-1, 0], [0, -1], [0, 1], [1, 0]])

    for y in range(1, sea_floor.shape[0] - 1):
        for x in range(1, sea_floor.shape[1] - 1):
            point = sea_floor[y, x]
            neighbourhood = [sea_floor[y + y_off, x + x_off] for y_off, x_off in neighbours]
            if point < np.min(neighbourhood):
                is_minimum[y, x] = True

    risk_level = np.sum(np.multiply(sea_floor, is_minimum)) + np.count_nonzero(is_minimum)
    return risk_level, is_minimum


def find_basins(sea_floor, minima):
    """
    Find the basins by starting from the local minima, and checking the four neighbours.
    If the neighbour is below 9, add it to the current basin. Repeat until no new neighbours are added.
    This assumes only one minimum per basin! (Which is correct for this puzzle)
    """
    neighbours = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    basins = []
    for y, x in list(zip(*np.nonzero(minima))):
        basin = [(y, x)]
        while True:
            new = []
            for yy, xx in basin:
                for yoff, xoff in neighbours:
                    ny, nx = yy + yoff, xx + xoff
                    if sea_floor[ny, nx] < 9 and (ny, nx) not in basin and (ny, nx) not in new:
                        new.append((ny, nx))
            if len(new) == 0:
                break
            else:
                basin += new
        basins.append(basin)
    return basins   
    
    
def main():
    input_raw = (Path.cwd() / "input.txt").read_text()
    sea_floor = np.array([[int(x) for x in line] for line in input_raw.split('\n')[:-1]])

    # Create a wall around the measured sea floor which will never be the minimum.
    # This makes it easier to deal with the boundaries.
    padded = np.pad(sea_floor, 1, mode='constant', constant_values=10)

    # Part 1
    risk_level, minima = calculate_risk(padded)
    print("Answer part 1:", risk_level)

    # Part 2
    basins = find_basins(padded, minima)
    three_largest_basins = sorted(basins, key=lambda x: len(x), reverse=True)[:3]
    print("Answer part 2:", np.prod([len(x) for x in three_largest_basins]))


if __name__ == "__main__":
    main()

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint
from scipy.ndimage.morphology import binary_erosion as erode
from scipy.ndimage.morphology import binary_dilation as dilate
from scipy.ndimage.morphology import binary_opening as open
from scipy.ndimage.morphology import binary_closing as close


def plot_sea_floor(sea_floor):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    X = np.arange(0, sea_floor.shape[1], 1)
    Y = np.arange(0, sea_floor.shape[0], 1)
    X, Y = np.meshgrid(X, Y)

    ax.plot_surface(X, Y, sea_floor, alpha=0.2)
    plt.show()


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
    return risk_level


def main():
    input_raw = (Path.cwd() / "input.txt").read_text()
    sea_floor = np.array([[int(x) for x in line] for line in input_raw.split('\n')[:-1]])
    # plot_sea_floor(sea_floor)

    # Create a wall around the measured sea floor which will never be the minimum.
    # This makes it easier to deal with the boundaries.
    padded = np.pad(sea_floor, 1, mode='constant', constant_values=10)

    # Part 1
    print("Answer part 1:", calculate_risk(padded))

    # Part 2
    # I don't do pathfinding, thanks.


if __name__ == "__main__":
    main()

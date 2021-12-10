import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint


def main():
    input_raw = (Path.cwd() / "input.txt").read_text()
    input_split = input_raw.split('\n')[:-1]
    lines = [[tuple(int(x) for x in p.split(',')) for p in line.split(' -> ')] for line in input_split]
    dirs = [(line[0][0] - line[1][0] // max(abs(line[0][0] - line[1][0]), abs(line[1][0] - line[1][1])),
             line[1][0] - line[1][1] // max(abs(line[0][0] - line[1][0]), abs(line[1][0] - line[1][1])))
            for line in lines]

    grid = np.zeros((988, 988))

    print(dirs)
    for line, dir in zip(lines, dirs):
        if sum(dir) == 1:
            current = line[0]
            # print(current)
            while current != line[1]:
                grid[current[0], current[1]] += 1
                current[0] += dir[0]
                current[1] += dir[1]
                print(current)
        # break
    plt.imshow(grid)
    plt.show()




if __name__ == "__main__":
    main()

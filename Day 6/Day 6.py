import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint


def simulate_growth(initial_state):
    fish = initial_state

    for day in range(1, 81):
        fish -= 1
        new_spawn_count = np.count_nonzero(fish == -1)
        fish = fish[fish >= 0]
        baby_fish = np.ones(new_spawn_count)*8
        parent_fish = np.ones(new_spawn_count)*6
        # print(new_spawn_count, len(baby_fish), len(parent_fish))
        fish = np.append(fish, baby_fish)
        fish = np.append(fish, parent_fish)
        print(f"After day {day} there are {len(fish)} fish.")


def optimized_simulation(initial_state):
    # 1884401676620 is too high.

    fish = {day: amount for day, amount in zip(list(range(9)), [0]*9)}
    values, counts = np.unique(initial_state, return_counts=True)
    for days, amounts in zip(values, counts):
        fish[days] = amounts

    for day in range(1, 256):
        new_spawn_count = fish[0]
        for days, amounts in fish.items():
            if days > 0:
                fish[days-1] = fish[days]
        fish[8] = new_spawn_count
        fish[6] += new_spawn_count

        print(f"After day {day} there are {sum(fish.values())} fish.")


def main():
    input_raw = (Path.cwd() / "input.txt").read_text()
    fish = np.array(input_raw.split(',')).astype(np.int)

    # Part 1
    simulate_growth(fish)

    # Part 2
    optimized_simulation(fish)


if __name__ == "__main__":
    main()

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint
import imageio

# Is it octopi, octopuses or something else? In this house, it is octos.


def create_gif(image_folder: Path, name: str):
    images = [imageio.imread(file) for file in image_folder.glob('*.png')]
    imageio.mimsave(image_folder/name, images)


def step(octos):
    # Add a charge to all octos.
    octos += 1

    # Keep track of octos that have already flashed.
    has_flashed = np.zeros_like(octos, dtype=np.bool)

    # Find the positions of octos with a charge above 9.
    charged_octos = list(zip(*np.nonzero(octos > 9)))

    flashes = 0

    while True:
        for y, x in charged_octos:
            if not has_flashed[y, x]:
                # Add a charge to the 3x3 neighbourhood.
                octos[max(y-1, 0):y+2, max(x-1, 0):x+2] += 1
                has_flashed[y, x] = True
                flashes += 1


        # Check for octos that are now charged.
        charged_octos = list(zip(*np.nonzero(np.multiply(octos, ~has_flashed) > 9)))

        # If no charged octos are found, quit.
        if len(charged_octos) == 0:
            break

    # Set the discharged octos to 0.
    octos = np.multiply(octos, ~has_flashed)
    return octos, flashes


def main():
    input_raw = (Path.cwd() / "input.txt").read_text()
    lines = input_raw.split('\n')

    octos = np.array([[int(energy) for energy in line] for line in lines])

    # Set up extra stuff to export the images to make a GIF from it.
    # It looks pretty cool! (Takes a little while though).
    make_gif = False
    folder = Path.cwd() / 'images_part_1'
    if make_gif:
        folder.mkdir(exist_ok=True)
        plt.imshow(octos)
        plt.savefig(folder/'0.png')

    total = 0
    for i in range(100):
        octos, flashes = step(octos)

        if make_gif:
            plt.imshow(octos)
            plt.savefig(folder/f'{i+1}.png')
            plt.close()

        total += flashes

    print("Answer part 1:", total)
    if make_gif:
        create_gif(folder, 'part1.gif')


if __name__ == "__main__":
    main()

import os

import matplotlib.pyplot as plt
import numpy as np


class CoveragePlanner:
    """
    0 uncut grass
    1 obstacle
    2 cut grass
    """
    DIRECTION_PREFERENCE = ['left', 'down', 'up', 'right']

    def __init__(self, grid):
        self._grid = np.pad(grid, 1, constant_values=1)
        unique, counts = np.unique(grid, return_counts=True)
        self._unmowed = counts[1]
        self._path = []

    def _find_closest(self, i, j):
        r, c = np.nonzero(self._grid == 0)
        min_idx = (abs(r - i) + abs(c - j)).argmin()
        return r[min_idx], c[min_idx]

    def _get_next_position(self, i, j):
        if self._grid[i, j - 1] == 0:
            return i, j - 1
        if self._grid[i + 1, j] == 0:
            return i + 1, j
        if self._grid[i - 1, j] == 0:
            return i - 1, j
        if self._grid[i, j + 1] == 0:
            return i, j + 1
        return None

    def start(self):
        i, j = self._find_closest(1, 1)
        plt.cla()
        img = plt.imshow(self._grid[1:-1, 1:-1], vmin=0, vmax=2)
        while True:
            while self._grid[i, j] < 1:
                self._unmowed -= 1
                self._grid[i, j] = 2
                self._path.append((i, j))
                position = self._get_next_position(i, j)
                if position is None:
                    print('Stop')
                    break
                i, j = position
                img.set_data(self._grid[1:-1, 1:-1])
                plt.pause(0.01)
            if self._unmowed == 0:
                print('Finished')
            i, j = self._find_closest(i, j)


def main():
    #grid = np.load('grid_image.npy')
    grid = plt.imread(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'map', 'test_2.png'))
    grid = 1 - grid  # revert pixel values
    planner = CoveragePlanner(grid)

    #planner._find_closest(15, 7)

    planner.start()
    #plt.imshow(planner._grid)
    #plt.show()


if __name__ == '__main__':
    main()
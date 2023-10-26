import random
# random.seed(0)

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label


COMPONENT_STRUCTURE = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])


class Grid:
    def __init__(self, grid):
        self._grid = grid
        self._h, self._w = self._grid.shape

    @property
    def grid(self):
        return self._grid

    def place_obstacle(self, obstacle):
        obstacle_h, obstacle_w = obstacle.shape
        tries = 0
        while tries < 20:
            tries += 1
            i = random.randint(0, self._h - obstacle_h)
            j = random.randint(0, self._w - obstacle_w)
            _, components_orig = label(self._grid, COMPONENT_STRUCTURE)
            self._grid[i:i+obstacle_h, j:j+obstacle_w] += obstacle

            if np.unique(self._grid).shape[0] > 2:  # placement collision:
                self._grid[i:i+obstacle_h, j:j+obstacle_w] -= obstacle
                continue
            _, components_new = label(self._grid, COMPONENT_STRUCTURE)
            if components_new <= components_orig:  # no new component created
                self._grid[i:i+obstacle_h, j:j+obstacle_w] -= obstacle
                continue
            return True
        return False


def generate_grid_simple(width, height, obstacle_density):
    grid = np.zeros(width * height, dtype=float)
    obstacles = random.sample(range(width * height), int(obstacle_density * width * height))
    grid[obstacles] = 1
    return grid.reshape((width, height))


def generate_grid(width, height, obstacle_density, min_size=1, max_size=1):
    grid = Grid(np.zeros((width, height), dtype=float))
    to_fill = int(obstacle_density * width * height)
    tries = 0
    while to_fill > 0 and tries < width * height:
        print(to_fill)
        tries += 1
        obstacle_size = random.randint(min_size, max_size)
        obstacle = generate_obstacle(obstacle_size)
        if grid.place_obstacle(obstacle):
            to_fill -= obstacle_size
    if tries > width * height:
        raise ValueError('Generation failed')
    return grid.grid


def generate_obstacle(size):
    def get_open_neighbours(pos):
        tmp_neighbours = []
        if pos[0] > 0 and grid[pos[0] - 1, pos[1]] == 0:
            tmp_neighbours.append((pos[0] - 1, pos[1]))
        if pos[1] > 0 and grid[pos[0], pos[1] - 1] == 0:
            tmp_neighbours.append((pos[0], pos[1] - 1))
        if pos[0] < width - 1 and grid[pos[0] + 1, pos[1]] == 0:
            tmp_neighbours.append((pos[0] + 1, pos[1]))
        if pos[1] < height - 1 and grid[pos[0], pos[1] + 1] == 0:
            tmp_neighbours.append((pos[0], pos[1] + 1))
        return tmp_neighbours

    width = size
    height = size
    grid = np.zeros((width, height))
    start = (width // 2, height // 2)
    grid[start] = 1
    open_neighbours = get_open_neighbours(start)
    for i in range(size - 1):
        selected_neighbour_idx = random.randint(1, len(open_neighbours)) - 1
        selected_neighbour = open_neighbours[selected_neighbour_idx]

        grid[selected_neighbour] = 1
        del open_neighbours[selected_neighbour_idx]
        open_neighbours.extend(get_open_neighbours(selected_neighbour))
        open_neighbours = list(set(open_neighbours))

    for row_idx in reversed(range(size)):
        if np.sum(grid[row_idx, :]) == 0:
            grid = np.delete(grid, row_idx, 0)

    for col_idx in reversed(range(size)):
        if np.sum(grid[:, col_idx]) == 0:
            grid = np.delete(grid, col_idx, 1)

    return grid


def plot_grid(grid):
    labeled, ncomponents = label(grid, COMPONENT_STRUCTURE)
    plt.imshow(labeled)
    plt.savefig('grid.png')


if __name__ == '__main__':
    # grid = generate_grid_simple(10, 10, 0.4)
    grid = generate_grid(20, 20, 0.4, 4, 20)
    plot_grid(grid)

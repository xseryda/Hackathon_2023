import os

import matplotlib.pyplot as plt
import numpy as np


DRAW_STEP = 100


class GRASS_STATE:
    OBSTACLE = 0


class Agent:
    def __init__(self, agent_id, grid, i, j):
        self._id = agent_id
        self._grid = grid
        self._i = i
        self._j = j

    @property
    def i(self):
        return self._i

    @property
    def j(self):
        return self._j

    def get_next_position(self, i, j):
        if self._grid[i, j - 1] == 0:  # TODO use ID here
            return i, j - 1
        if self._grid[i + 1, j] == 0:
            return i + 1, j
        if self._grid[i - 1, j] == 0:
            return i - 1, j
        if self._grid[i, j + 1] == 0:
            return i, j + 1
        return None

    def set_position(self, i, j):
        self._i = i
        self._j = j


class CoveragePlanner:
    """
    0 Obstacle
    >0 planned for agent i
    <0 mowed by agent i
    """
    DIRECTION_PREFERENCE = ['left', 'down', 'up', 'right']

    def __init__(self, grid):
        self._agents = []
        self._grid = np.pad(grid, 1, constant_values=1)
        unique, counts = np.unique(grid, return_counts=True)
        self._unmowed = counts[0]
        self._path = []

    def _find_closest(self, i, j):
        r, c = np.nonzero(self._grid == 0)
        min_idx = (abs(r - i) + abs(c - j)).argmin()
        return r[min_idx], c[min_idx]

    def add_agent(self, i, j):
        i, j = self._find_closest(i, j)
        agent_id = len(self._agents) + 1
        self._agents.append(Agent(agent_id, self._grid, i, j))

    def start(self):
        plt.cla()
        img = plt.imshow(self._grid[1:-1, 1:-1], vmin=-len(self._agents),
                         vmax=len(self._agents))
        step = 0
        while True:
            for agent in self._agents:
                i, j = agent.i, agent.j
                if self._grid[i, j] < 1:
                    self._unmowed -= 1
                    self._grid[i, j] = 2
                    self._path.append((i, j))
                    position = agent.get_next_position(i, j)
                    if position is None:
                        print('Stop')
                        continue
                    step += 1
                    i, j = position
                    agent.set_position(i, j)
                    if step % DRAW_STEP == 0:
                        img.set_data(self._grid[1:-1, 1:-1])
                        plt.pause(0.01)
                if self._unmowed == 0:
                    print('Finished')
                    return
                agent.set_position(*self._find_closest(i, j))


def main():
    grid = np.load('grid_image.npy')
    #grid = plt.imread(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'map', 'test_3.png'))
    #grid = 1 - grid  # revert pixel values
    planner = CoveragePlanner(grid)
    planner.add_agent(1, 1)
    planner.add_agent(grid.shape[0], 1)

    planner.start()


if __name__ == '__main__':
    main()

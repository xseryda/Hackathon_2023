import json

import matplotlib.pyplot as plt
import numpy as np

from BFS import BFS


DRAW_STEP = 100


class GrassState:
    OBSTACLE = 0


class Agent:
    def __init__(self, agent_id, grid, i, j):
        self._bfs = BFS(grid)
        self._id = agent_id
        self._grid = grid
        self._path = [(i, j)]
        self._i = i
        self._j = j
        self._unmowed = 0

    @property
    def active(self):
        return self._unmowed > 0

    @property
    def id(self):
        return self._id

    @property
    def i(self):
        return self._i

    @property
    def j(self):
        return self._j

    @property
    def path(self):
        return self._path

    @property
    def unmowed(self):
        return self._unmowed

    @unmowed.setter
    def unmowed(self, value):
        self._unmowed = value

    def extend_path(self, i, j):
        self._path.append((i, j))
        self._unmowed -= 1

    def get_next_position(self, i, j):
        if self._grid[i, j - 1] == self.id:
            return i, j - 1
        if self._grid[i + 1, j] == self.id:
            return i + 1, j
        if self._grid[i - 1, j] == self.id:
            return i - 1, j
        if self._grid[i, j + 1] == self.id:
            return i, j + 1
        return None

    def move_to_unmowed(self):
        path = self._bfs.find_path((self.i, self.j), self.id)
        self._path.extend(path)
        self.set_position(*path[-1])

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
        self._grid = np.pad(grid, 1, constant_values=GrassState.OBSTACLE)
        self._unmowed = None
        self._path = []

    @property
    def agents(self):
        return self._agents

    def add_agent(self):
        agent_id = len(self._agents) + 1
        i_ind, j_ind = (self._grid == agent_id).nonzero()
        j_min = j_ind.argmin()
        i, j = int(i_ind[j_min]), int(j_ind[j_min])  # start with position where j minial
        self._agents.append(Agent(agent_id, self._grid, i, j))

    def start(self):
        unique, counts = np.unique(self._grid, return_counts=True)
        self._unmowed = 0
        for i, agent in enumerate(self._agents, start=1):
            agent.unmowed = counts[i]
            self._unmowed += agent.unmowed
        img = plt.imshow(self._grid[1:-1, 1:-1], vmin=-len(self._agents),
                         vmax=len(self._agents) + 1)
        step = 0
        while True:
            for agent in self._agents:
                if self._unmowed == 0:
                    print('Finished')
                    return
                i, j = agent.i, agent.j
                if self._grid[i, j] == agent.id:
                    self._unmowed -= 1
                    self._grid[i, j] = -agent.id
                    agent.extend_path(i, j)
                    if not agent.active:
                        continue
                    position = agent.get_next_position(i, j)
                    if position is None:
                        print(f'Stop {agent.id=}')
                        agent.move_to_unmowed()
                        continue
                    step += 1
                    i, j = position
                    agent.set_position(i, j)
                    if step % DRAW_STEP == 0:
                        img.set_data(self._grid[1:-1, 1:-1])
                        # plt.savefig(f'pictures/{step:06d}.png')
                        plt.pause(0.01)


def main():
    grid = np.load('grid_color.npy')
    #grid = plt.imread(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'map', 'test_3.png'))
    #grid = 1 - grid  # revert pixel values
    planner = CoveragePlanner(grid)
    planner.add_agent()
    planner.add_agent()
    planner.add_agent()
    planner.add_agent()

    planner.start()
    paths = []
    for agent in planner.agents:
        print(len(agent.path))
        paths.append(agent.path)
    with open('paths.json', 'w') as f:
        json.dump(paths, f)


if __name__ == '__main__':
    main()

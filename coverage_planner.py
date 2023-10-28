import json

import matplotlib.pyplot as plt
import numpy as np

from BFS import BFS
from skeleton import generate_skeleton, Directions


DRAW_STEP = 10
NUM_AGENTS = 4


class GrassState:
    OBSTACLE = 0


class Agent:
    def __init__(self, agent_id, grid, skelet, i, j):
        self._bfs = BFS(grid)
        self._id = agent_id
        self._last_direction = None
        self._grid = grid
        self._path = [(i, j)]
        self._skelet = skelet
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

    def move(self):
        def move_by_direction(direction):
            i, j = self.i + direction[0], self.j + direction[1]
            # print(f'Move to {direction}, {i=}, {j=}')
            self._grid[i, j] = -self.id
            self.extend_path(i, j)
            self.set_position(i, j)

        if not self.active:
            return

        skeleton_direction = self._skelet.direction(self.i - 1, self.j - 1)  # -1 to acount for padding
        if self._last_direction is None or self._last_direction == skeleton_direction:
            move_by_direction(skeleton_direction)
            move_by_direction(skeleton_direction)
        elif self._last_direction == Directions.reverse(skeleton_direction):  # wraparound, trace branch back
            move_by_direction(self._last_direction)
            if skeleton_direction in (Directions.UP, Directions.DOWN):
                move_by_direction(Directions.LEFT if (self.j - 1) % 2 else Directions.RIGHT)
            else:
                move_by_direction(Directions.UP if (self.i - 1) % 2 else Directions.DOWN)
            move_by_direction(skeleton_direction)
            move_by_direction(skeleton_direction)
        else:  # corner turn
            if (skeleton_direction == Directions.RIGHT and (self.j - 1) % 2 == 0 or
                    skeleton_direction == Directions.LEFT and (self.j - 1) % 2 == 1 or
                    skeleton_direction == Directions.DOWN and (self.i - 1) % 2 == 0 or
                    skeleton_direction == Directions.UP and (self.i - 1) % 2 == 1):  # long turn
                move_by_direction(self._last_direction)
                move_by_direction(skeleton_direction)
                move_by_direction(skeleton_direction)
            else:  # short turn
                move_by_direction(skeleton_direction)
        self._last_direction = skeleton_direction


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

    def add_agents(self, count):
        for counter in range(count):
            agent_id = len(self._agents) + 1
            i_ind, j_ind = (self._grid == agent_id).nonzero()
            j_min = j_ind.argmin()
            i, j = int(i_ind[j_min]), int(j_ind[j_min])  # start with position where j minial
            skelet = generate_skeleton(self._grid[1:-1, 1:-1], 1)
            self._agents.append(Agent(agent_id, self._grid, skelet, i, j))

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
                agent.move()
                step += 1
                if step % DRAW_STEP == 0:
                    img.set_data(self._grid[1:-1, 1:-1])
                    # plt.savefig(f'pictures/{step:06d}.png')
                    plt.pause(0.01)


def main():
    grid = np.load(f'grid_color_{NUM_AGENTS}.npy')
    #grid = plt.imread(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'map', 'test_3.png'))
    #grid = 1 - grid  # revert pixel values
    planner = CoveragePlanner(grid)
    planner.add_agents(1)

    planner.start()
    paths = []
    for agent in planner.agents:
        print(len(agent.path))
        paths.append(agent.path)
    with open('paths.json', 'w') as f:
        json.dump(paths, f)


if __name__ == '__main__':
    main()

import pickle

import cv2
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

NUM_AGENTS = 4
WEIGHT_HOR, WEIGHT_VER = 5, 1


def reduce_grid(grid, agent_id=0):
    """
    Get recuted grid by factor 2. If any cell in the reduced cell is obstacle, the whole new cell is marked as obstacle.
    0 means obstacle
    1 means free path
    """
    height_red, width_red = grid.shape[0] // 2, grid.shape[1] // 2
    grid_red = np.zeros((height_red, width_red))
    for i_red in range(height_red):
        for j_red in range(width_red):
            if grid[i_red * 2, j_red * 2] != agent_id:
                continue
            if grid[i_red * 2 + 1, j_red * 2] != agent_id:
                continue
            if grid[i_red * 2, j_red * 2 + 1] != agent_id:
                continue
            if grid[i_red * 2 + 1, j_red * 2 + 1] != agent_id:
                continue
            grid_red[i_red, j_red] = 1
    return grid_red


def expand_grid(grid):
    height_exp, width_exp = grid.shape[0] * 2, grid.shape[1] * 2
    grid_exp = np.zeros((height_exp, width_exp))
    for i in range(height_exp):
        for j in range(width_exp):
            grid_exp[i, j] = grid[i // 2, j // 2]
    return grid_exp


def generate_skeleton(grid: np.array, agent_id: int):
    height_red, width_red = grid.shape[0] // 2, grid.shape[1] // 2
    grid_red = reduce_grid(grid, agent_id)

    cs_graph = np.zeros((grid.size // 4, grid.size // 4))

    for i_red in range(height_red):
        for j_red in range(width_red):
            if not grid_red[i_red, j_red]:
                continue
            cs_ind = i_red * width_red + j_red
            if j_red > 0 and grid_red[i_red, j_red - 1]:  # left
                cs_graph[cs_ind, cs_ind - 1] = WEIGHT_HOR
            # if j_red < width_red - 1 and grid_red[i_red, j_red + 1]:  # right
            #     cs_graph[cs_ind, cs_ind + 1] = WEIGHT_HOR
            if i_red > 0 and grid_red[i_red - 1, j_red]:  # up
                cs_graph[cs_ind, cs_ind - width_red] = WEIGHT_VER
            # if i_red < height_red - 1 and grid_red[i_red, j_red + 1]:  # down
            #     cs_graph[cs_ind, cs_ind + width_red] = WEIGHT_VER
    cs_graph_skelet = minimum_spanning_tree(cs_graph).toarray()
    return Skeleton(cs_graph_skelet, height_red, width_red)


class Directions:
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @classmethod
    def reverse(cls, direction):
        if direction == cls.UP:
            return cls.DOWN
        if direction == cls.DOWN:
            return cls.UP
        if direction == cls.RIGHT:
            return cls.LEFT
        if direction == cls.LEFT:
            return cls.RIGHT


class Skeleton:
    def __init__(self, cs_graph, height_red, width_red):
        """
        Matrix lower triangular, check only lower triangle (i > j).
        """
        self._h_red = height_red
        self._w_red = width_red
        self._cs_graph = cs_graph
        self._last_direction = None

    @property
    def cs_graph(self):
        return self._cs_graph

    def _get_directions(self, i_red, j_red):
        directions = []

        cs_ind = i_red * self._w_red + j_red
        if j_red > 0 and self._cs_graph[cs_ind, cs_ind - 1]:
             directions.append(Directions.LEFT)
        if j_red < self._w_red - 1 and self._cs_graph[cs_ind + 1, cs_ind]:
             directions.append(Directions.RIGHT)
        if i_red > 0 and self._cs_graph[cs_ind, cs_ind - self._w_red]:
             directions.append(Directions.UP)
        if i_red < self._h_red - 1 and self._cs_graph[cs_ind + self._w_red, cs_ind]:
             directions.append(Directions.DOWN)
        return directions

    def direction(self, grid_i, grid_j):
        i_red, j_red = grid_i // 2, grid_j // 2
        directions = self._get_directions(i_red, j_red)
        print(directions)
        if self._last_direction is None:
            preferences = [Directions.LEFT, Directions.DOWN, Directions.RIGHT, Directions.UP]
        elif self._last_direction == Directions.DOWN:
            preferences = [Directions.LEFT, Directions.DOWN, Directions.RIGHT, Directions.UP]
        elif self._last_direction == Directions.UP:
            preferences = [Directions.RIGHT, Directions.UP, Directions.LEFT, Directions.DOWN]
        elif self._last_direction == Directions.LEFT:
            preferences = [Directions.UP, Directions.LEFT, Directions.DOWN, Directions.RIGHT]
        else:  # right
            preferences = [Directions.DOWN, Directions.RIGHT, Directions.UP, Directions.LEFT]
        for preference in preferences:
            if preference in directions:
                self._last_direction = preference
                return preference
        raise ValueError
        

def plot_skelet(grid, cs_skelet):
    height_red, width_red = grid.shape[0] // 2, grid.shape[1] // 2
    grid_image_path = 'res/garden.png'
    # Load the grid image
    grid_image = cv2.imread(grid_image_path)

    rescale_x = grid_image.shape[0] / 100
    rescale_y = grid_image.shape[1] / 150
    drawn = 0
    for i, j in zip(*cs_skelet.cs_graph.nonzero()):
        drawn += 1
        #if drawn > 100:
        #    break
        i_start, j_start = int(rescale_y*(i // width_red)), int(rescale_x*(i % width_red))
        i_end, j_end = int(rescale_y*(j // width_red)), int(rescale_x*(j % width_red))
        cv2.line(grid_image, (j_start, i_start), (j_end, i_end), (255, 0, 0), 2)
    # result_image = cv2.resize(grid_image, [1300, 600])
    cv2.imshow('Agent Path', grid_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    grid = np.load(f'grid_color_{NUM_AGENTS}.npy')
    cs_skelet = generate_skeleton(grid, 4)
    plot_skelet(grid, cs_skelet)
    #with open('skelets.pkl', 'wb') as f:
    #    pickle.dump([cs_skelet], f)


if __name__ == '__main__':
    main()

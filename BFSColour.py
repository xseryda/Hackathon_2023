import numpy as np

from skeleton import reduce_grid, expand_grid


class BFSColour:
    def __init__(self, grid):
        self.grid = grid

    def _get_neighbours(self, node):
        neighbours = []
        if node[0] > 0:
            neighbours.append((node[0] - 1, node[1]))
        if node[1] > 0:
            neighbours.append((node[0], node[1] - 1))
        if node[0] < self.grid.shape[0] - 1:
            neighbours.append((node[0] + 1, node[1]))
        if node[1] < self.grid.shape[1] - 1:
            neighbours.append((node[0], node[1] + 1))
        return neighbours

    def divide_grid(self, starts):
        def validate_inputs():
            """
            Here grid 0 means grass, 1 means obstacle
            """
            for start in starts:
                i, j = start
                assert self.grid[i, j] == 0

        validate_inputs()
        agents = list(range(len(starts)))
        closed_nodes = []
        open_nodes = []
        cost = np.copy(self.grid) * self.grid.size
        divided_grid = np.copy(self.grid) * self.grid.size
        for idx, start in enumerate(starts, start=1):
            open_nodes.append([start])
            cost[start] = 0
            divided_grid[start] = idx

        while any(open_nodes):
            for i in agents:
                if not open_nodes[i]:
                    print(f"Agent {i + 1} finished")
                    agents.remove(i)
                    continue
                current = open_nodes[i].pop(0)
                closed_nodes.append(current)
                for neighbour in self._get_neighbours(current):
                    if neighbour in closed_nodes:
                        continue
                    if divided_grid[neighbour] != 0:  # already assigned or obstacle
                        continue  # move only on dedicated cells or non-mowed cells
                    neighbour_cost = cost[current] + 1
                    if neighbour not in open_nodes[i]:
                        open_nodes[i].append(neighbour)
                    elif bool(neighbour_cost >= cost[neighbour] != 0):
                        continue
                    divided_grid[neighbour] = i + 1
                    cost[neighbour] = neighbour_cost

        return divided_grid


if __name__ == '__main__':
    #image = np.load('grid_image.npy')
    import matplotlib.pyplot as plt
    import cv2

    grid = plt.imread('res/grid_image_red.png')
    grid = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)

    grid = reduce_grid(grid)
    grid = 1-grid

    bfs = BFSColour(grid)

    #agents = [(0, 0), (0, 150), (0, 299), (199, 0), (199, 150), (199, 299)]
    height, width = grid.shape
    agents = [(0, 0), (0, width-1), (height-1, 0), (height-1, width-1)]
    result = bfs.divide_grid(agents)

    result[result == 0] = len(agents) + 1
    result[result == grid.size] = 0

    result = expand_grid(result)  # TODO reduce + expand simplifies the grid, problematic points are removed

    img = plt.imshow(result)
    np.save(f'grid_color_{len(agents)}.npy', result)

    plt.savefig('test.png')

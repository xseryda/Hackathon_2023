from queue import Queue
import numpy as np


class BFSColour:
    def __init__(self, grid):
        self.grid = grid

    def divide_grid(self, starts):
        def get_neighbours(node):
            if node[0] > 0:
                yield node[0] - 1, node[1]
            if node[1] > 0:
                yield node[0], node[1] - 1
            if node[0] < self.grid.shape[0] - 1:
                yield node[0] + 1, node[1]
            if node[1] < self.grid.shape[1] - 1:
                yield node[0], node[1] + 1

        agents = list(range(len(starts)))
        closed_nodes = []
        open_nodes = []
        cost = np.copy(self.grid) * self.grid.size
        divided_grid = np.zeros(self.grid.shape)
        for idx, start in enumerate(starts, start=1):
            q = Queue()
            q.put(start)
            open_nodes.append(q)
            cost[start] = 0
            divided_grid[start] = idx

        while agents:
            for i in agents:
                if open_nodes[i].empty():
                    print(f"Agent {i + 1} finished")
                    agents.remove(i)
                    continue
                current = open_nodes[i].get()
                closed_nodes.append(current)
                for neighbour in get_neighbours(current):
                    if neighbour in closed_nodes:
                        continue
                    if divided_grid[neighbour] != i and self.grid[neighbour] != 0:
                        continue  # move only on dedicated cells or non-mowed cells
                    neighbour_cost = cost[current] + 1
                    if bool(neighbour_cost >= cost[neighbour] != 0):
                        continue
                    open_nodes[i].put(neighbour)
                    divided_grid[neighbour] = i + 1
                    cost[neighbour] = neighbour_cost

        return divided_grid


if __name__ == '__main__':
    image = np.load('grid_image.npy')
    a_star = BFSColour(image)
    np.save('grid_image_color.npy', a_star.divide_grid([(0, 0), (0, 299), (199, 0), (199, 299)]))

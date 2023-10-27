import numpy as np


class BFSColour:
    def __init__(self, grid):
        self.grid = grid

    def divide_grid(self, starts):
        def get_neighbours(node):
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
                for neighbour in get_neighbours(current):
                    if neighbour in closed_nodes:
                        continue
                    if divided_grid[neighbour] != i and self.grid[neighbour] != 0:
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
    image = np.load('grid_image.npy')
    a_star = BFSColour(image)
    print(a_star.divide_grid([(0, 0), (0, 299), (199, 0), (199, 299)]))

import numpy as np


class BFS:
    def __init__(self, grid):
        self.grid = grid

    def find_path(self, start: tuple, target: int):
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

        def get_result_path(end):
            result = []
            tmp = end
            while tmp != start:
                result.append(tmp)
                tmp = came_from[tmp]
            return list(reversed(result))

        closed_nodes = []
        open_nodes = [start]
        cost = np.copy(self.grid) * self.grid.size
        cost[start] = 0
        came_from = {}

        while open_nodes:
            current = open_nodes.pop(0)
            if self.grid[current] == target:
                return get_result_path(current)
            closed_nodes.append(current)
            for neighbour in get_neighbours(current):
                if neighbour in closed_nodes:
                    continue
                if abs(self.grid[neighbour]) != target and self.grid[neighbour] != 0:
                    continue  # move only on dedicated cells or non-mowed cells
                neighbour_cost = cost[current] + 1
                if neighbour not in open_nodes:
                    open_nodes.append(neighbour)
                elif bool(neighbour_cost >= cost[neighbour] != 0):
                    continue
                came_from[neighbour] = current
                cost[neighbour] = neighbour_cost

        raise FileNotFoundError("Cesta nenalezena :D")


if __name__ == '__main__':
    image = np.load('grid_image.npy')
    image[(199, 299)] = 2
    a_star = BFS(image)
    print(a_star.find_path((0, 0), 2))

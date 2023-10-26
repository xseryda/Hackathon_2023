import numpy as np
import math

X_MAX = 1920
Y_MAX = 1080


def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


class AStar:
    def __init__(self, grid):
        self.grid = grid

    def find_path(self, start, end):
        def get_closest_open():
            closest = open_nodes[0]
            for open_node in open_nodes[1:]:
                if cost_f[open_node] < cost_f[closest]:
                    closest = open_node
            return closest

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

        def get_result_path():
            result = []
            tmp = end
            while tmp != start:
                result.append(tmp)
                tmp = came_from[tmp]
            return list(reversed(result))


        closed_nodes = []
        open_nodes = [start]
        cost_g = np.copy(self.grid) * self.grid.size
        cost_f = np.copy(self.grid) * self.grid.size
        cost_g[start] = 0
        cost_f[start] = manhattan_distance(start, end)
        # cost_f[start] = math.dist(start, end)
        came_from = {}

        while open_nodes:
            current = get_closest_open()
            if current == end:
                return get_result_path()
            open_nodes.remove(current)
            closed_nodes.append(current)
            for neighbour in get_neighbours(current):
                if neighbour in closed_nodes:
                    continue
                neighbour_cost = cost_g[current] + 1
                if neighbour not in open_nodes and cost_g[neighbour] != self.grid.size:
                    open_nodes.append(neighbour)
                elif bool(neighbour_cost <= cost_g[neighbour] != 0):
                    continue
                came_from[neighbour] = current
                cost_g[neighbour] = neighbour_cost
                cost_f[neighbour] = manhattan_distance(neighbour, end)
                # cost_f[neighbour] = math.dist(neighbour, end)

        raise FileNotFoundError("Cesta nenalezena :D")


if __name__ == '__main__':
    a_star = AStar(np.load('grid_image.npy'))
    print(a_star.find_path((0, 0), (199, 299)))

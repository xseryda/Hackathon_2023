import random

def generate_grid(rows, columns, obstacle_density, obstacle_size):
    grid = []
    for _ in range(rows):
        row = []
        for _ in range(columns):
            if random.random() < obstacle_density:
                # Generate an obstacle of the specified size
                for _ in range(obstacle_size):
                    row.append(1)  # 1 represents an obstacle
            else:
                row.extend([0] * obstacle_size)  # 0 represents an empty space
        grid.append(row)
    return grid

# Example usage:
rows = 10
columns = 10
obstacle_density = 0.3
obstacle_size = 4  # Set the obstacle size
grid = generate_grid(rows, columns, obstacle_density, obstacle_size)

for row in grid:
    print(row)

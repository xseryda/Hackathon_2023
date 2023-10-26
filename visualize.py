import cv2
import numpy as np

def visualize_agent_path(grid_image_path, start, end, path_points):
    # Load the grid image
    grid_image = cv2.imread(grid_image_path)

    if grid_image is None:
        print("Grid image not found or could not be loaded.")
        return

    # Copy the grid image for visualization
    path_image = grid_image.copy()

    # Create a list of points representing the agent's path
    path = [(start[0], start[1])]

    # Sample path points (you should replace this with your multi-path planning logic)
    for i in range(1, path_points + 1):
        x = int(start[0] + (end[0] - start[0]) * i / path_points)
        y = int(start[1] + (end[1] - start[1]) * i / path_points)
        path.append((x, y))

    # Draw the path on the path_image
    for i in range(1, len(path)):
        cv2.line(path_image, path[i - 1], path[i], (0, 0, 255), 7)

    # Display the path image with the agent's red path
    cv2.imshow('Agent Path', path_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example of how to call the function:
if __name__ == "__main__":
    grid_image_path = 'garden.png'
    start_point = (10, 10)
    end_point = (290, 190)
    path_points = 100
    visualize_agent_path(grid_image_path, start_point, end_point, path_points)

import cv2
import numpy as np

def visualize_agent_path(grid_image_path, start, end, path_points, color='blue', transparency=0.5):
    # Load the grid image
    grid_image = cv2.imread(grid_image_path)

    if grid_image is None:
        print("Grid image not found or could not be loaded.")
        return

    # Create a transparent overlay image
    overlay_image = grid_image.copy()

    # Create a list of points representing the agent's path
    path = [(start[0], start[1])]

    # Sample path points (you should replace this with your multi-path planning logic)
    for i in range(1, path_points + 1):
        x = int(start[0] + (end[0] - start[0]) * i / path_points)
        y = int(start[1] + (end[1] - start[1]) * i / path_points)
        path.append((x, y))

    # Define color mappings
    color_mapping = {
        'blue': (255, 0, 0),
        'orange': (0, 115, 255),
        'green': (0, 255, 0),
        'red': (0, 0, 255),
        'black': (0, 0, 0)
    }

    # Check if the specified color is valid
    if color in color_mapping:
        line_color = color_mapping[color]
    else:
        print("Invalid color specified. Using blue by default.")
        line_color = color_mapping['blue']

    # Draw the semi-transparent path with the specified color on the overlay image
    for i in range(1, len(path)):
        cv2.line(overlay_image, path[i - 1], path[i], line_color, 7) 

    # Blend the overlay image with the original image
    result_image = cv2.addWeighted(overlay_image, transparency, grid_image, 1 - transparency, 0)

    # Display the result image with the agent's semi-transparent path
    cv2.imshow('Agent Path', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example of how to call the function with different colors:
#if __name__ == "__main__":
#    grid_image_path = 'garden.png'
#    start_point = (10, 10)
#    end_point = (1000, 1000)
#    path_points = 100

    # Specify the color when calling the function ('blue', 'orange', 'green', 'red', or 'black')
    #visualize_agent_path(grid_image_path, start_point, end_point, path_points, color='blue')
    #visualize_agent_path(grid_image_path, start_point, end_point, path_points, color='orange')
    #visualize_agent_path(grid_image_path, start_point, end_point, path_points, color='green')
    #visualize_agent_path(grid_image_path, start_point, end_point, path_points, color='red')
    #visualize_agent_path(grid_image_path, start_point, end_point, path_points, color='black')

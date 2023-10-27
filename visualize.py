import json

import cv2
import numpy as np

# Define color mappings
color_mapping = {
    'blue': (255, 0, 0),
    'orange': (0, 115, 255),
    'green': (0, 255, 0),
    'red': (0, 0, 255),
    'black': (0, 0, 0)
}


def visualize_agent_path(grid_image, path, color='blue', transparency=1):
    # Create a transparent overlay image
    overlay_image = grid_image.copy()

    rescale_x = grid_image.shape[0] / 200
    rescale_y = grid_image.shape[1] / 300
    for i in range(len(path)):
        path[i] = [int(path[i][1] * rescale_y), int(path[i][0] * rescale_x)]

    # Draw the semi-transparent path with the specified color on the overlay image
    for i in range(1, len(path)):
        cv2.line(overlay_image, path[i - 1], path[i], color, 2)

    # Blend the overlay image with the original image
    return overlay_image


def visualize_divided_grid(image, grid, no_agents, transparency=0.5):
    mask = np.zeros((*grid.shape, 3), dtype=np.uint8)

    mask[grid == 0] = color_mapping['black']
    colors = list(color_mapping.values())
    for i in range(no_agents):
        mask[grid == i + 1] = colors[i]
    mask[grid == no_agents + 1] = color_mapping['black']

    mask = cv2.resize(mask, [image.shape[1], image.shape[0]])
    # Apply the mask to the image using alpha blending
    return cv2.addWeighted(image, 1, mask, transparency, 0)


# Example of how to call the function with different colors:
if __name__ == "__main__":
    grid_image_path = 'garden.png'
    # Load the grid image
    grid_image = cv2.imread(grid_image_path)
    with open("paths.json") as f:
        paths = json.load(f)

    grid = np.load('grid_color.npy')

    # Specify the color when calling the function ('blue', 'orange', 'green', 'red', or 'black')

    colors = list(color_mapping.values())
    for idx, path in enumerate(paths):
        grid_image = visualize_agent_path(grid_image, path, color=colors[idx])

    result_image = visualize_divided_grid(grid_image, grid, 4, 0.3)

    # result_image = cv2.resize(result_image, [1300, 600])
    cv2.imwrite('result_image.jpg', result_image)
    cv2.imshow('Agent Path', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
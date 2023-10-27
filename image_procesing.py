import cv2
import numpy as np

# Load the image
image = cv2.imread('garden_fixed.png')

if image is None:
    print("Image not found or could not be loaded.")
else:
    image = cv2.blur(image, (40,40))
    #image = cv2.medianBlur(image, 10)
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper HSV ranges for green and yellow
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])

    lower_brown = np.array([10, 50, 50])  # Lower HSV values for brown
    upper_brown = np.array([30, 255, 255])  # Upper HSV values for brown

    # Create masks to isolate all shades of green and yellow
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    brown_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

    # Combine the masks to detect all shades of green and yellow
    combined_mask = cv2.bitwise_or(green_mask, yellow_mask)
    combined_mask = cv2.bitwise_or(combined_mask, brown_mask)

    # Invert the mask so that all shades of green and yellow become white (1) and the rest becomes black (0)
    kernel = np.ones((7, 7), np.uint8)
    combined_mask2 = cv2.erode(combined_mask, kernel, iterations=0)

    inverted_mask = cv2.bitwise_not(combined_mask2)

    # Erode the mask to ignore single pixels
    
     
    # Resize the inverted mask to the desired grid size (300x200)
    grid_size = (300, 200)
    resized_mask = cv2.resize(inverted_mask, grid_size)

    resized_mask[resized_mask > 0] = 255

    # Save the grid as an image
    cv2.imwrite('grid_image.png', resized_mask)

    resized_mask[resized_mask > 0] = 1
    np.save('grid_image.npy', resized_mask)

    print("Grid image has been saved to 'grid_image.png'.")

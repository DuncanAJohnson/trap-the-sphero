import cv2 as cv
import numpy as np

def get_sphero_position(frame):
    """
    Detect the largest white region in an image and return its center coordinates.

    Args:
        frame (np.array): The input frame.

    Returns:
        tuple: Center coordinates of the largest white region (x, y) or None if no region is found.
    """

    # Convert to HSV to better detect the white regions
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Define the range for white color in HSV
    lower_white = np.array([0, 15, 230])
    upper_white = np.array([240, 35, 255])
    # lower_orange = np.array([5, 150, 150])
    # upper_orange = np.array([45, 255, 255])

    # Create a mask to isolate white areas
    white_mask = cv.inRange(hsv_frame, lower_white, upper_white)

    # cv.imshow("White Mask", white_mask)
    # cv.waitKey(0)

    # Find contours of the white regions
    contours, _ = cv.findContours(white_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour by area
        largest_contour = max(contours, key=cv.contourArea)

        # Get the bounding box of the largest contour
        x, y, w, h = cv.boundingRect(largest_contour)

        # Calculate the center of the bounding box
        center_x = x + w // 2
        center_y = y + h // 2

        # Draw the bounding box and the center on the frame (for visualization)
        cv.drawContours(frame, [largest_contour], -1, (0, 255, 0), 3)
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Mark the center

        # Display the result
        # cv.imshow("Original Frame", frame)
        # cv.imshow("White Mask", white_mask)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        return (center_x, center_y)
    else:
        print("No white regions found.")
        return None
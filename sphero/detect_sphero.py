import cv2 as cv
import numpy as np
import threading
import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

# Function to move the Sphero to a direction for a certain distance
def move(api, direction, distance):
    """
    Move the Sphero in the specified direction for the given distance.
    Print the direction and distance moved.

    Args:
        api (SpheroEduAPI): The Sphero API object.
        direction (int): The direction to move (in degrees).
        distance (float): The distance to move (in centimeters).
    """
    # Define direction names for better readability
    directions = {0: "right", 90: "down", 180: "left", 270: "up"}
    
    # Print the direction and distance
    print(f"Moving {directions.get(direction, 'unknown direction')} for {distance} centimeters.")
    
    api.set_heading(direction)  # Set the heading direction (0=right, 90=down, 180=left, 270=up)
    start = api.get_distance()
    api.set_speed(100)

    while True:
        rolled_cm = api.get_distance() - start
        if rolled_cm > distance:
            api.set_speed(0)
            break

    # Print the completed movement information
    print(f"Movement complete. Rolled {rolled_cm:.2f} centimeters.")

# Find and connect to the toy
toy = scanner.find_toy(toy_name="SB-A644")
if not toy:
    print("No Sphero found!")
    exit()

# Define target position for Sphero (as an example)
target_position = {"x": 400, "y": 200}

# Main program
frame = cv.imread("my_photo-2.jpg")
if frame is None:
    print("Failed to load image")
    exit()

prevCircle = None

# Distance calculation function for tracking
dist = lambda x1, y1, x2, y2: (x1 - x2)**2 + (y1 - y2)**2

# Define the minimum and maximum area thresholds (you can adjust these)
min_area = 5  # Minimum contour area
max_area = 100  # Maximum contour area (you can adjust this)

# Start the Sphero API connection and control
with SpheroEduAPI(toy) as api:
    # Set the LED to white on connection
    api.set_main_led(Color(r=255, g=255, b=255))

    # Convert to HSV to better detect the white regions
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Define the range for white color in HSV
    lower_white = np.array([0, 0, 200])  # Lower bound for white color
    upper_white = np.array([180, 30, 255])  # Upper bound for white color

    # Create a mask to isolate white areas
    white_mask = cv.inRange(hsv_frame, lower_white, upper_white)

    # Optional: Invert the mask to exclude white areas if needed (depends on your application)
    inverted_mask = cv.bitwise_not(white_mask)

    # Mask out the white regions from the frame
    masked_frame = cv.bitwise_and(frame, frame, mask=inverted_mask)

    # Display the original frame and the white mask
    cv.imshow("Original Frame", frame)
    cv.imshow("White Mask", white_mask)
    cv.imshow("Inverted White Mask", inverted_mask)
    cv.imshow("Masked Frame", masked_frame)

    # Convert the masked frame to grayscale
    grey_frame = cv.cvtColor(masked_frame, cv.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale frame to reduce noise
    blur_frame = cv.GaussianBlur(grey_frame, (17, 17), 0)

    # Find contours of the white regions
    contours, _ = cv.findContours(white_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Variable to track the largest contour
    largest_contour = None
    max_area_found = 0

    # If contours are found
    if contours:
        # Loop over each contour
        for contour in contours:
            # Calculate the area of the contour
            area = cv.contourArea(contour)

            # If the area is within the desired range
            if min_area <= area <= max_area:
                # Track the largest contour
                if area > max_area_found:
                    largest_contour = contour
                    max_area_found = area

    # If we have a valid largest contour
    if largest_contour is not None:
        # Get the bounding box of the largest contour
        x, y, w, h = cv.boundingRect(largest_contour)

        # Calculate the center of the bounding box
        center_x = x + w // 2
        center_y = y + h // 2

        # Draw the bounding box and the center on the frame
        cv.drawContours(frame, [largest_contour], -1, (0, 255, 0), 3)
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Mark the center

        # Print the center coordinates
        print(f"Center coordinates: ({center_x}, {center_y})")

        # Calculate the distance to the target position
        target_x = target_position["x"]
        target_y = target_position["y"]

        dx = target_x - center_x
        dy = target_y - center_y
        print(f"Horizontal distance: {dx} pixels")
        print(f"Vertical distance: {dy} pixels")

        # Move horizontally (right or left)
        if dx > 0:
            move(api, 0, dx/5)  # Move right
        else:
            move(api, 180, abs(dx/5))  # Move left

        # Move vertically (up or down)
        if dy > 0:
            move(api, 90, dy/5)  # Move down
        else:
            move(api, 270, abs(dy/5))  # Move up
        move(api, 180, abs(dx/5))  # Move left
        move(api, 270, abs(dy/5))  # Move up

    # Display the final frame with the largest white region and center marked
    cv.imshow("Filtered White Regions", frame)

    # Wait for a keypress to proceed or quit
    key = cv.waitKey(0) & 0xFF
    if key == ord('q'):  # Press 'q' to quit
        exit()

# Clean up
cv.destroyAllWindows()

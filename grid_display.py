import cv2
import numpy as np
from cv.detect_squares import detect_squares

# HSV color range for grid tape
BLUE_LOWER_RANGE = (100, 110, 50)  # Adjust based on tape color and lighting
BLUE_UPPER_RANGE = (140, 255, 255)  # Adjust based on tape color and lighting
GRID_TAPE_COLOR_RANGE = (BLUE_LOWER_RANGE, BLUE_UPPER_RANGE)

# size range for grid squares
GRID_SQUARE_SIZE_RANGE = (30, 40)

def display_filters(frame):
    # Convert to HSV
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Conversion', frame_hsv)

    # Apply color mask to extract blue (grid tape)
    mask = cv2.inRange(frame_hsv, GRID_TAPE_COLOR_RANGE[0], GRID_TAPE_COLOR_RANGE[1])
    cv2.imshow('Color Mask', mask)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(mask, (3, 3), 0)
    cv2.imshow('Blurred Mask', blurred)

    # Edge detection using Canny
    median = np.median(blurred)
    lower_thresh = int(max(0, 0.66 * median))
    upper_thresh = int(min(255, 1.33 * median))
    edges = cv2.Canny(blurred, lower_thresh, upper_thresh)
    cv2.imshow('Edge Detection (Canny)', edges)

    # Detect squares in the image (contours)
    centers = detect_squares(frame, GRID_TAPE_COLOR_RANGE, GRID_SQUARE_SIZE_RANGE)

    # Draw contours and centers on the image
    contour_img = frame.copy()
    for center in centers:
        cv2.circle(contour_img, tuple(map(int, center)), 10, (0, 0, 255), -1)

    cv2.imshow('Squares Detected', contour_img)

def main():
    # Load your test image (change the file path to your own image)
    image_path = 'images/blue_grid.png'
    frame = cv2.imread(image_path)

    # Display the filter results
    display_filters(frame)

    # Wait for a key press to close the image windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

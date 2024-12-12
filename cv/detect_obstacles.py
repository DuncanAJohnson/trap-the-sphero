from cv.detect_squares import detect_squares

# hsv color range for obstacles - wider range to catch more orange shades
ORANGE_LOWER_RANGE = (0, 100, 100)     # Include more reddish-orange
ORANGE_UPPER_RANGE = (35, 255, 255)    # Include more yellowish-orange
OBSTACLE_COLOR_RANGE = (ORANGE_LOWER_RANGE, ORANGE_UPPER_RANGE)

# size range for obstacles
OBSTACLE_SIZE_RANGE = (400, 900)

# detects the centers of the obstacles in the image
def detect_obstacles(frame):
    return detect_squares(frame, OBSTACLE_COLOR_RANGE, OBSTACLE_SIZE_RANGE)

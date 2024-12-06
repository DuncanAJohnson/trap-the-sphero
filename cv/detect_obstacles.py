from cv.detect_squares import detect_squares

# color range for obstacles
BLUE_LOWER_RANGE = (50, 0, 0)
BLUE_UPPER_RANGE = (255, 50, 50)
OBSTACLE_COLOR_RANGE = (BLUE_LOWER_RANGE, BLUE_UPPER_RANGE)

# size range for obstacles
OBSTACLE_SIZE_RANGE = (300, 1000)

# detects the centers of the obstacles in the image
def detect_obstacles(frame):
    return detect_squares(frame, OBSTACLE_COLOR_RANGE, OBSTACLE_SIZE_RANGE)

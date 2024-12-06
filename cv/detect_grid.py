from cv.detect_squares import detect_squares

# color range for grid tape
BLACK_LOWER_RANGE = (0, 0, 0)
BLACK_UPPER_RANGE = (60, 60, 60)
GRID_TAPE_COLOR_RANGE = (BLACK_LOWER_RANGE, BLACK_UPPER_RANGE)

# size range for grid squares
GRID_SQUARE_SIZE_RANGE = (1500, 3500)

# detects the centers of the grid squares in the image
def detect_grid_squares(frame):
    return detect_squares(frame, GRID_TAPE_COLOR_RANGE, GRID_SQUARE_SIZE_RANGE)

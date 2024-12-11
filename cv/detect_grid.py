from cv.detect_squares import detect_squares

# HSV color range for grid tape
BLACK_LOWER_RANGE = (0, 0, 0)        # Any hue, no saturation, very dark
BLACK_UPPER_RANGE = (60, 60, 60)    # Any hue, low saturation, dark values
GRID_TAPE_COLOR_RANGE = (BLACK_LOWER_RANGE, BLACK_UPPER_RANGE)

# size range for grid squares
GRID_SQUARE_SIZE_RANGE = (300, 900)

# detects the centers of the grid squares in the image and returns a 2D array of the centers
def detect_grid_squares(frame):
    centers = detect_squares(frame, GRID_TAPE_COLOR_RANGE, GRID_SQUARE_SIZE_RANGE, False)
    
    # Sort centers by y coordinate first (top to bottom)
    centers.sort(key=lambda p: p[1])
    
    # Determine grid dimensions by analyzing point distributions
    y_coords = [p[1] for p in centers]
    rows = 1
    for i in range(1, len(y_coords)):
        if abs(y_coords[i] - y_coords[i-1]) > 20:  # threshold for new row
            rows += 1
    
    cols = len(centers) // rows
    if rows * cols != len(centers):
        raise ValueError(f"Number of centers ({len(centers)}) cannot be arranged in a grid")
    
    # Create rows by taking cols points at a time and sorting each row by x coordinate
    grid = []
    for i in range(0, len(centers), cols):
        row = centers[i:i+cols]
        row.sort(key=lambda p: p[0])  # Sort row by x coordinate (left to right)
        grid.append(row)
    
    return grid
    
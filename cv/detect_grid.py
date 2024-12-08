from cv.detect_squares import detect_squares

# color range for grid tape
BLACK_LOWER_RANGE = (0, 0, 0)
BLACK_UPPER_RANGE = (60, 60, 60)
GRID_TAPE_COLOR_RANGE = (BLACK_LOWER_RANGE, BLACK_UPPER_RANGE)

# size range for grid squares
GRID_SQUARE_SIZE_RANGE = (1500, 3500)

# detects the centers of the grid squares in the image and returns a 2D array of the centers
def detect_grid_squares(frame):
    centers = detect_squares(frame, GRID_TAPE_COLOR_RANGE, GRID_SQUARE_SIZE_RANGE)
    
    # Calculate grid size (n x n)
    n = int(len(centers) ** 0.5)
    if n * n != len(centers):
        raise ValueError(f"Number of centers ({len(centers)}) is not a perfect square")
    
    # Sort centers by y coordinate first (top to bottom)
    centers.sort(key=lambda p: p[1])
    
    # Create rows by taking n points at a time and sorting each row by x coordinate
    grid = []
    for i in range(0, len(centers), n):
        row = centers[i:i+n]
        row.sort(key=lambda p: p[0])  # Sort row by x coordinate (left to right)
        grid.append(row)
    
    return grid
    
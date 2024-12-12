from pathfinding.a_star import a_star_search
from utils.classes import Pathfinding_Environment

def find_edge_squares(environment: Pathfinding_Environment):
    edge_squares = []

    # Collect only the edge squares
    for x in range(environment.grid_size[0]):
        edge_squares.append((x, 0))  # Top edge
        edge_squares.append((x, environment.grid_size[1] - 1))  # Bottom edge

    for y in range(environment.grid_size[1]):
        edge_squares.append((0, y))  # Left edge
        edge_squares.append((environment.grid_size[0] - 1, y))  # Right edge

    return edge_squares

def make_grid(environment: Pathfinding_Environment):
    grid = [[1 for _ in range(environment.grid_size[0])] for _ in range(environment.grid_size[1])]

    # set obstacles to 0 to mark them as blocked
    for obstacle in environment.obstacles:
        grid[obstacle[0]][obstacle[1]] = 0

    print(grid)

    return grid

# given the current environment, find the next square for the sphero to move to
def find_next_square(environment: Pathfinding_Environment):
    edge_squares = find_edge_squares(environment)

    grid = make_grid(environment)

    # pathfind to all squares on the edge of the grid
    min_steps = float('inf')
    next_square_to_move_to = None
    for square in edge_squares:
        # print("Searching from ", environment.sphero, " to ", square)
        # print(grid)
        grid_copy = grid.copy()
        next_square, steps = a_star_search(grid_copy, environment.sphero, square)
        # print("Next square: ", next_square)
        if steps < min_steps:
            min_steps = steps
            next_square_to_move_to = next_square
        # print(next_square_to_move_to)

    return next_square_to_move_to
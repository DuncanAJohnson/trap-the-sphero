# print the path in ascii art
def visualize_path(path, sphero, obstacles, grid_width, grid_height):
    # create a 2D array to represent the grid
    grid = [['_' for _ in range(grid_width)] for _ in range(grid_height)]

    # add the sphero to the grid
    grid[sphero[1]][sphero[0]] = 'S'
    
    # add the obstacles to the grid
    for obstacle in obstacles:
        grid[obstacle[1]][obstacle[0]] = 'O'

    for point in path:
        grid[point[1]][point[0]] = 'x'
    
    # print the grid
    for row in grid:
        print(''.join(str(cell) for cell in row))
    
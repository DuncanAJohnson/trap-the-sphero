import visualize_path

sphero = (2, 2)
obstacles = [(1, 1), (2, 1)]
path = [(1, 2), (0, 2), (0, 1), (0, 0)]
grid_width = 5
grid_height = 5

visualize_path.visualize_path(path, sphero, obstacles, grid_width, grid_height)
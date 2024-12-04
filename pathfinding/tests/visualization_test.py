from classes import Pathfinding_Environment

sphero = (2, 2)
obstacles = [(1, 1), (2, 1)]
grid_size = (5, 5)

environment = Pathfinding_Environment(sphero, obstacles, grid_size)

print(environment)
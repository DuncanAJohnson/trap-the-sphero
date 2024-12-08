from utils.classes import Pathfinding_Environment
from pathfinding.pathfinding import find_next_square

sphero = (2, 2)
obstacles = [(1, 1), (2, 1), (1, 2), (1, 3), (2, 3), (4, 2)]
grid_size = (5, 5)

environment = Pathfinding_Environment(sphero, obstacles, grid_size)
print("~~~Initial environment~~~")
print(environment)


# repeat until the sphero reaches the edge of the grid (because then it will definitely escape)
while not (environment.sphero[0] == 0 or environment.sphero[0] == environment.grid_size[0] - 1 or environment.sphero[1] == 0 or environment.sphero[1] == environment.grid_size[1] - 1):
    next_square = find_next_square(environment)
    environment.sphero = next_square

    if next_square is None:
        print("Sphero is trapped!")
        break

    print("~~~Next environment~~~")
    print(environment)

if next_square is not None:
    print("Sphero escaped!")


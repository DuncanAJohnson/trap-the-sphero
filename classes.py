from dataclasses import dataclass


@dataclass
class Grid_Square:
    corners: list[tuple[int, int]]
    center: tuple[int, int]

@dataclass
class Pathfinding_Environment:
    sphero: tuple[int, int]
    obstacles: list[tuple[int, int]]
    grid_size: tuple[int, int]

    # print the environment in ascii art
    def __str__(self):
        # create a 2D array to represent the grid
        grid = [['_' for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]

        # add the sphero to the grid
        grid[self.sphero[1]][self.sphero[0]] = 'S'

        # add the obstacles to the grid
        for obstacle in self.obstacles:
            grid[obstacle[1]][obstacle[0]] = 'O'

        # create a string representation of the grid
        grid_str = '\n'.join(''.join(str(cell) for cell in row) for row in grid)
        return grid_str  # Return the string representation
    
import asyncio
from utils.classes import Pathfinding_Environment
from utils.camera import take_picture
from cv.detect_grid import detect_grid_squares
from cv.detect_sphero import get_sphero_position
from cv.detect_obstacles import detect_obstacles
from pathfinding.pathfinding import find_next_square
from sphero.sphero import Sphero

GRID_SIZE = (5, 5)
num_obstacles = 0
grid_centers = None
sphero = None
turn = "Human"
win = None
movement_complete = False
# find the grid coordinates of the closest grid center
def find_grid_coords(center):
    closest_center = min(grid_centers, key=lambda x: distance(x, center))
    return closest_center

def get_pathfinding_environment(frame):
    # get the sphero's position
    sphero_image_position = get_sphero_position(frame)

    # get the obstacles' positions
    obstacles_image_positions = detect_obstacles(frame)

    # find the grid coordinate of the sphero and obstacles
    sphero_grid_position = find_grid_coords(sphero_image_position)
    obstacles_grid_positions = [find_grid_coords(obstacle) for obstacle in obstacles_image_positions]

    # return the pathfinding environment
    return Pathfinding_Environment(sphero_grid_position, obstacles_grid_positions, GRID_SIZE)

def game_start():
    # take a picture of the grid
    frame = take_picture()

    # get the grid square centers
    grid_centers = detect_grid_squares(frame)

    # initialize the sphero
    sphero = Sphero()


async def game_loop():
    if turn == "Human":
        # wait until another obstacle is added to the grid
        obstacles = detect_obstacles(frame)
        if len(obstacles) > num_obstacles:
            turn = "Sphero"
        return
    
    if turn == "Sphero":
        # get the sphero's position and the pathfinding environment
        pathfinding_environment = get_pathfinding_environment(frame)

        # check if the sphero has escaped
        if pathfinding_environment.sphero[0] == 0 or pathfinding_environment.sphero[0] == pathfinding_environment.grid_size[0] - 1 or pathfinding_environment.sphero[1] == 0 or pathfinding_environment.sphero[1] == pathfinding_environment.grid_size[1] - 1:
            win = "Sphero"
            return

        # get the path
        next_square = find_next_square(pathfinding_environment)

        # check if the sphero is trapped
        if next_square is None:
            win = "Human"
            return

        while not movement_complete:
            # get the sphero's position
            sphero_image_position = get_sphero_position(frame)

            # move the sphero towards the image coordinates of the next square
            movement_complete = await sphero.move_sphero(sphero_image_position, grid_centers[next_square])

        turn = "Human"
        sphero.stop_sphero()
        movement_complete = False
    

if __name__ == "__main__":
    game_start()
    while win is None:
        asyncio.run(game_loop())

    if win == "Human":
        print("Human wins!")
    elif win == "Sphero":
        print("Sphero wins!")
    else:
        print("Error: no winner")
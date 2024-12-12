import time
from utils.classes import Pathfinding_Environment
from utils.camera import Camera
from cv.detect_grid import detect_grid_squares
from cv.detect_sphero import get_sphero_position
from cv.detect_obstacles import detect_obstacles
from pathfinding.pathfinding import find_next_square
from sphero.move_sphero import SpheroController
from sphero.sphero import Sphero
from spherov2.sphero_edu import SpheroEduAPI
import cv2
import numpy as np
from spherov2.types import Color


class Game:
    def __init__(self):
        self.GRID_SIZE = (5, 5)
        self.num_obstacles = 0
        self.grid_centers = None
        self.sphero = None
        self.turn = "Human"
        self.win = None
        self.movement_complete = False
        self.X_BOUNDS = (155, 505)
        self.Y_BOUNDS = (150, 450)
        self.CAMERA_INDEX = 2
        self.camera = None

    def distance(self, point_1, point_2):
        return (point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2

    # find the grid coordinates of the closest grid center
    def find_grid_coords(self, center):
        grid_centers_list = []
        for i, row in enumerate(self.grid_centers):
            for j, point in enumerate(row):
                grid_centers_list.append((i, j, point))  # Include row and column indices with the point

        # Find the closest grid center
        closest_center = min(grid_centers_list, key=lambda x: self.distance(x[2], center))  # x[2] is the point

        # Return the index (i, j) of the closest center
        return closest_center[0], closest_center[1]


    def get_pathfinding_environment(self, frame):
        # get the sphero's position
        sphero_image_position = get_sphero_position(frame)

        # get the obstacles' positions
        obstacles_image_positions = detect_obstacles(frame)

        # find the grid coordinate of the sphero and obstacles
        sphero_grid_position = self.find_grid_coords(sphero_image_position)
        print("Sphero grid pos: ", sphero_grid_position)
        obstacles_grid_positions = [self.find_grid_coords(obstacle) for obstacle in obstacles_image_positions]

        # return the pathfinding environment
        return Pathfinding_Environment(sphero_grid_position, obstacles_grid_positions, self.GRID_SIZE)

    def game_start(self):
        # initialize the camera
        self.camera = Camera(self.X_BOUNDS, self.Y_BOUNDS, self.CAMERA_INDEX)

        # take a picture of the grid
        frame = self.camera.take_picture()

        # cv2.imshow("First picture", frame)
        # cv2.waitKey(0)
        
        # get the grid square centers
        self.grid_centers = detect_grid_squares(frame)

        print("Grid Centers: ", self.grid_centers)

        # initialize the sphero
        self.sphero = SpheroController("SB-A644")

    def game_loop(self, api):
        # self.sphero.set_color()

        if self.turn == "Human":
            # set greento say human turn
            self.sphero.set_color(api, Color(r=0, g=255, b=0))
            # wait until someone enters a button to indicate end of turn
            input("Press Enter when human done")
            self.turn = "Sphero"
            return
        
        if self.turn == "Sphero":
            frame = None
            self.sphero.set_color(api, Color(r=255, g=255, b=255))

            frame = self.camera.take_picture()

            cv2.imshow("Capture before movement", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # get the sphero's position and the pathfinding environment
            pathfinding_environment = self.get_pathfinding_environment(frame)

            print(pathfinding_environment)

            # check if the sphero has escaped
            if pathfinding_environment.sphero[0] == 0 or pathfinding_environment.sphero[0] == pathfinding_environment.grid_size[0] - 1 or pathfinding_environment.sphero[1] == 0 or pathfinding_environment.sphero[1] == pathfinding_environment.grid_size[1] - 1:
                self.win = "Sphero"
                return

            # get the path
            next_square = find_next_square(pathfinding_environment)
            print("Moving to ", next_square)

            # check if the sphero is trapped
            if next_square is None:
                self.win = "Human"
                return

            while not self.movement_complete:
                # get the sphero's position
                frame = self.camera.take_picture()
                
                sphero_image_position = get_sphero_position(frame)

                # move the sphero towards the image coordinates of the next square
                self.movement_complete = self.sphero.move_to_target(api, sphero_image_position, self.grid_centers[next_square[0]][next_square[1]])

            self.turn = "Human"
            self.sphero.stop_sphero(api)
            self.movement_complete = False
        

if __name__ == "__main__":
    game = Game()
    game.game_start()
    with SpheroEduAPI(game.sphero.toy) as api:
        game.sphero.set_color(api, Color(r=255, b=255, g=255))
        api.set_heading(0)
        while game.win is None:
            game.game_loop(api)

    if game.win == "Human":
        print("Human wins!")
    elif game.win == "Sphero":
        print("Sphero wins!")
    else:
        print("Error: no winner")
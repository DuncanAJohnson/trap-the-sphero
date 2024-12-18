import cv2 as cv
import numpy as np
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
import time
import math

class SpheroController:
    """
    A utility class to control the Sphero robot based on detected positions.
    """
    def __init__(self, toy_name):
        """
        Initialize the SpheroController with the specified toy name.

        Args:
            toy_name (str): The name of the Sphero toy to connect to.
        """
        print("Sphero Connecting...")
        self.toy = scanner.find_toy(toy_name=toy_name)
        if not self.toy:
            print("No Sphero found!")
            exit()

    def set_color(self, api, color):
        api.set_main_led(color)
        time.sleep(1)

    def move_to_target_old(self, api, center, target_position):
        """
        Move the Sphero to the target position based on the detected center.

        Args:
            center (tuple): The detected center coordinates (x, y).
            target_position (dict): The target position as a dictionary with 'x' and 'y'.
        """

        dx = target_position[0] - center[0]
        dy = target_position[0] - center[1]

        def move(api, direction, distance):
            directions = {0: "right", 90: "down", 180: "left", 270: "up"}
            print(f"Moving {directions.get(direction, 'unknown direction')} for {distance} centimeters.")
            api.set_heading(direction)
            start = api.get_distance()
            api.set_speed(100)

            while True:
                rolled_cm = api.get_distance() - start
                if rolled_cm > distance:
                    api.set_speed(0)
                    break

            print(f"Movement complete. Rolled {rolled_cm:.2f} centimeters.")

        # Move horizontally
        if dx > 0:
            move(api, 0, dx / 5)
        else:
            move(api, 180, abs(dx / 5))

        # Move vertically
        if dy > 0:
            move(api, 90, dy / 5)
        else:
            move(api, 270, abs(dy / 5))
    
    def move_to_target(self, api, center, target_position):
        # print("Moving from ", center, " to ", target_position)
        # check if the sphero is close to the next square using cartesian distance
        distance_to_next_square = (center[0] - target_position[0])**2 + (center[1] - target_position[1])**2
        if (distance_to_next_square < 20**2):
            return True

        # calculate the difference between the current position and the desired position
        diff = (target_position[0] - center[0], target_position[1] - center[1])

        # convert the difference to a direction
        direction = math.degrees(math.atan2(diff[1], diff[0]))

        # print("Diff to move: ", diff, " and heading is now ", direction)

        api.set_heading(int(direction))

        api.set_speed(17)

        return False

    def stop_sphero(self, api):
        api.set_speed(0)
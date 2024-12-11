import cv2 as cv
import numpy as np
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

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
        print("We are here")
        self.toy = scanner.find_toy(toy_name="SB-A644")
        if not self.toy:
            print("No Sphero found!")
            exit()

    def move_to_target(self, center, target_position):
        """
        Move the Sphero to the target position based on the detected center.

        Args:
            center (tuple): The detected center coordinates (x, y).
            target_position (dict): The target position as a dictionary with 'x' and 'y'.
        """
        with SpheroEduAPI(self.toy) as api:
            api.set_main_led(Color(r=255, g=255, b=255))

            dx = target_position['x'] - center[0]
            dy = target_position['y'] - center[1]

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
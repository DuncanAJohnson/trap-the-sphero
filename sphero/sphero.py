from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
import math

class Sphero:
    def __init__(self):
        self.previous_positions = []
        self.discount_factor = 0.8
        self.positions_to_average = 10
        self.DISTANCE_THRESHOLD = 10

        # Find and connect to the toy
        self.toy = scanner.find_toy(toy_name="SB-A644")
        if not self.toy:
            raise Exception("No Sphero found!")
        SpheroEduAPI(self.toy).set_main_led(Color(r=255, g=255, b=255))


    def move_sphero(self, detected_position, desired_position):
        # add the detected position to the list of previous positions
        self.previous_positions.append(detected_position)

        # if there are more than 10 previous positions, remove the oldest one
        if len(self.previous_positions) > self.positions_to_average:
            self.previous_positions.pop(0)

        # Calculate weighted average of positions (most recent positions have higher weight)
        weights = [self.discount_factor ** i for i in range(len(self.previous_positions)-1, -1, -1)]
        weight_sum = sum(weights)
        current_position = tuple(
            int(sum(p[i] * w for p, w in zip(self.previous_positions, weights)) / weight_sum)
            for i in range(2)
        )
        print("Current believed position: {}".format(current_position))

        # check if the sphero is close to the next square using cartesian distance
        distance_to_next_square = (current_position[0] - desired_position[0])**2 + (current_position[1] - desired_position[1])**2
        if (distance_to_next_square < self.DISTANCE_THRESHOLD**2):
            return True

        # calculate the difference between the current position and the desired position
        diff = (desired_position[0] - current_position[0], desired_position[1] - current_position[1])

        # convert the difference to a direction
        direction = math.atan2(diff[1], diff[0])

        SpheroEduAPI(self.toy).set_heading(direction)
        SpheroEduAPI(self.toy).set_speed(self.MAX_SPEED)

    def stop_sphero(self):
        SpheroEduAPI(self.toy).set_speed(0)
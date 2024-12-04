from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
import sys
import time


def say_hello(sphero, name):
    msg = "Hello! My name is {}. I can do a lot of cool stuff! I can say Hello"
    print(msg.format(name))

    for c in "Hello":
        sphero.set_matrix_character(c, Color(255, 0, 0))
        time.sleep(0.2)

    sphero.clear_matrix()


def point_north(sphero):
    print("If you calibrate my compass I can tell you which direction is north")
    sphero.calibrate_compass()
    sphero.set_compass_direction(0)
    color = Color(0, 255, 0)

    for _ in range(3):
        time.sleep(0.2)
        sphero.set_matrix_line(3, 0, 3, 7, color)
        sphero.set_matrix_line(4, 0, 4, 7, color)
        sphero.set_matrix_pixel(2, 6, color)
        sphero.set_matrix_pixel(5, 6, color)
        time.sleep(0.3)
        sphero.clear_matrix()


def roll(sphero, distance_cm):
    print("I can roll!")

    start = sphero.get_distance()
    sphero.set_speed(100)

    while True:
        rolled_cm = sphero.get_distance() - start
        if rolled_cm > distance_cm:
            sphero.set_speed(0)
            break

    print("I rolled {} centimeters :D".format(rolled_cm))
    print("Going back")

    sphero.spin(180, 1)

    start = sphero.get_distance()
    sphero.set_speed(100)

    while True:
        rolled_cm = sphero.get_distance() - start
        if rolled_cm > distance_cm:
            sphero.set_speed(0)
            break

def sensors(sphero):
    location = sphero.get_location()
    msg = (
        "I can tel you my location relative to the start of "
        "the program: x: {x}, y: {y}"
    )
    print(msg.format(**location))
    print("But I spin a lot so it is not very accurate")


def main():
    name = sys.argv[-1]
    toy = scanner.find_toy(toy_name=name)
    with SpheroEduAPI(toy) as sphero:
        say_hello(sphero, name)
        point_north(sphero)
        roll(sphero, 100)
        sensors(sphero)


if __name__ == '__main__':
    main()
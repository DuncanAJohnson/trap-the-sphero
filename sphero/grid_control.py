from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from pynput import keyboard
from spherov2.types import Color
import threading
import time

# Find and connect to the toy
toy = scanner.find_toy(toy_name="SB-A644")
if not toy:
    print("No Sphero found!")
    exit()

DIR_UP = 0
DIR_LEFT = 270
DIR_DOWN = 180
DIR_RIGHT = 90

speed = 50

# Define the arrow bitmap as a list of lists
arrow_pattern = [
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# Set the matrix LED to display the arrow
def set_arrow_pattern(api, pattern, color_on=Color(0, 255, 0), color_off=Color(0, 0, 0)):
    for row in range(8):
        for col in range(8):
            color = color_on if pattern[row][col] else color_off
            api.set_matrix_pixel(row, col, color)

def move_square(api, direction):
    api.set_heading(direction)
    api.set_speed(speed)
    time.sleep(0.75)
    api.set_speed(0)

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # Stop the listener

    if key == keyboard.Key.up:
        move_square(api, DIR_UP)
    elif key == keyboard.Key.down:
        move_square(api, DIR_DOWN)
    elif key == keyboard.Key.left:
        move_square(api, DIR_LEFT)
    elif key == keyboard.Key.right:
        move_square(api, DIR_RIGHT)

def move_between_squares(cur_square, to_square):
    while cur_square["x"] < to_square["x"]:
        move_square(api, DIR_RIGHT)
        cur_square["x"] += 1
    while cur_square["x"] > to_square["x"]:
        move_square(api, DIR_LEFT)
        cur_square["x"] -= 1
    while cur_square["y"] < to_square["y"]:
        move_square(api, DIR_DOWN)
        cur_square["y"] += 1
    while cur_square["y"] > to_square["y"]:
        move_square(api, DIR_UP)
        cur_square["y"] -= 1

# Main program
with SpheroEduAPI(toy) as api:
    # Indicate connection
    api.set_heading(0)
    set_arrow_pattern(api, arrow_pattern)
    api.set_main_led(Color(r=255, g=0, b=0))

    cur_pos = { "x": 0, "y": 0 }
    target_pos = { "x": 4, "y": 4 }

    move_between_squares(cur_pos, target_pos)

    # Listen for keyboard input
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    # Cleanup
    api.set_speed(0)
    api.set_main_led(Color(r=255, g=0, b=0))
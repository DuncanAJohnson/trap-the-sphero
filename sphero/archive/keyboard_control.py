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

# Key state tracking
key_states = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
}

# Control Sphero in a separate thread
def sphero_control(api):
    speed = 50
    while True:
        if key_states["up"]:
            api.set_speed(speed)
        elif key_states["down"]:
            api.set_heading(api.get_heading() + 180)
            api.set_speed(speed)
        else:
            api.set_speed(0)

        if key_states["left"]:
            api.set_heading(api.get_heading() - 45)
        if key_states["right"]:
            api.set_heading(api.get_heading() + 45)

        time.sleep(0.1)  # Adjust for smooth control

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # Stop the listener

    if key == keyboard.Key.up:
        key_states["up"] = True
    elif key == keyboard.Key.down:
        key_states["down"] = True
    elif key == keyboard.Key.left:
        key_states["left"] = True
    elif key == keyboard.Key.right:
        key_states["right"] = True

def on_release(key):
    if key == keyboard.Key.up:
        key_states["up"] = False
    elif key == keyboard.Key.down:
        key_states["down"] = False
    elif key == keyboard.Key.left:
        key_states["left"] = False
    elif key == keyboard.Key.right:
        key_states["right"] = False

# Main program
with SpheroEduAPI(toy) as api:
    # Indicate connection
    api.set_main_led(Color(r=0, g=255, b=0))
    api.spin(360, 1)

    # Start control thread
    control_thread = threading.Thread(target=sphero_control, args=(api,), daemon=True)
    control_thread.start()

    # Listen for keyboard input
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # Cleanup
    api.set_speed(0)
    api.set_main_led(Color(r=255, g=0, b=0))

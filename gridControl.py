import cv2
import numpy as np
import threading
import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

stop_event = threading.Event()
sphero_position = {"x": None, "y": None}

def track_sphero():
    global sphero_position

    cap = cv2.VideoCapture(0)  # Ensure the correct camera index
    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        stop_event.set()
        return

    prev_circle = None
    dist = lambda x1, y1, x2, y2: (x1 - x2)**2 + (y1 - y2)**2  # Distance function

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Preprocess the frame
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_frame = cv2.GaussianBlur(grey_frame, (17, 17), 0)

        # Detect circles
        circles = cv2.HoughCircles(blur_frame, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
                                   param1=100, param2=30, minRadius=75, maxRadius=400)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            chosen_circle = None
            for i in circles[0, :]:
                if chosen_circle is None:
                    chosen_circle = i
                if prev_circle is not None:
                    # Choose the circle closest to the previous position
                    if dist(chosen_circle[0], chosen_circle[1], prev_circle[0], prev_circle[1]) > dist(i[0], i[1], prev_circle[0], prev_circle[1]):
                        chosen_circle = i

            # Draw the chosen circle
            if chosen_circle is not None:
                cv2.circle(frame, (chosen_circle[0], chosen_circle[1]), 1, (0, 100, 100), 3)
                cv2.circle(frame, (chosen_circle[0], chosen_circle[1]), chosen_circle[2], (255, 0, 255), 3)

                # Update the global position of the Sphero
                sphero_position["x"] = int(chosen_circle[0])
                sphero_position["y"] = int(chosen_circle[1])
                prev_circle = chosen_circle

        # Display the frame
        cv2.imshow("Sphero Tracking - Hough Circle", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break

    cap.release()
    cv2.destroyAllWindows()



def move(api, direction, duration):
    api.set_heading(direction)  # Set the heading direction (0=right, 90=down, 180=left, 270=up)
    api.set_speed(50)  # Set speed
    time.sleep(duration)  # Move for the given duration
    api.set_speed(0)  # Stop the Sphero

def sphero_control(api):
    global sphero_position

    target_position = {"x": 400, "y": 200}  # Target coordinates
    threshold = 20  # Threshold to stop movement
    speed = 50  # Speed for movement control
    duration = 1  # Duration to move for 1 second

    # Loop to control the movement
    while not stop_event.is_set():
        if sphero_position["x"] is not None and sphero_position["y"] is not None:
            current_x = sphero_position["x"]  # Current x position
            current_y = sphero_position["y"]  # Current y position

            # Calculate the difference (dx, dy) between current position and target
            dx = target_position["x"] - current_x
            dy = target_position["y"] - current_y

            # Decide movement on the x-axis (right or left)
            if abs(dx) > threshold:
                if dx > 0:
                    move(api, 0, duration)  # Move right
                elif dx < 0:
                    move(api, 180, duration)  # Move left

            # Decide movement on the y-axis (up or down)
            if abs(dy) > threshold:
                if dy > 0:
                    move(api, 90, duration)  # Move down
                elif dy < 0:
                    move(api, 270, duration)  # Move up

            # If no movement is needed, stop the Sphero
            if abs(dx) <= threshold and abs(dy) <= threshold:
                print(f"Sphero reached the target at ({target_position['x']}, {target_position['y']}).")
                api.set_speed(0)  # Stop movement
                time.sleep(0.1)
                continue

            # Print debug info for movement
            print(f"Moving Sphero to target: dx = {dx:.2f}, dy = {dy:.2f}")

        else:
            print("Sphero not detected. Waiting for position updates.")

        time.sleep(0.1)  # Control loop frequency

toy = scanner.find_toy(toy_name="SB-A644")
if not toy:
    print("Error: No Sphero found!")
    exit()

with SpheroEduAPI(toy) as api:
    api.set_main_led(Color(r=139, g=69, b=19))  # light white LED
    time.sleep(1)
    try:
        tracking_thread = threading.Thread(target=track_sphero, daemon=True)
        control_thread = threading.Thread(target=sphero_control, args=(api,), daemon=True)

        tracking_thread.start()
        control_thread.start()

        while not stop_event.is_set():
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        api.set_speed(0)
        api.set_main_led(Color(r=255, g=0, b=0))
        stop_event.set()
        tracking_thread.join()
        control_thread.join()

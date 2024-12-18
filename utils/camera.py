from utils.crop_frame import crop_frame
import cv2
import numpy as np
import time

class Camera:
    def __init__(self, X_BOUNDS, Y_BOUNDS, camera_index=0):
        self.X_BOUNDS = X_BOUNDS
        self.Y_BOUNDS = Y_BOUNDS
        self.cap = cv2.VideoCapture(camera_index)

        # Check if the camera opened successfully
        if not self.cap.isOpened():
            print(f"Failed to open camera {camera_index}")
            raise ValueError("Camera not accessible")

        # Adjust other camera settings for better image quality
        self.cap.set(cv2.CAP_PROP_EXPOSURE, 157)
        self.cap.set(cv2.CAP_PROP_GAIN, 0)
        self.cap.set(cv2.CAP_PROP_GAMMA, 100)
        self.cap.set(cv2.CAP_PROP_CONTRAST, 32)
        self.cap.set(cv2.CAP_PROP_SATURATION, 64)
        self.cap.set(cv2.CAP_PROP_TEMPERATURE, 0)
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 1)
        self.cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4600)

        print("Set Exposure")

    def take_picture(self):
        # Flush the buffer by reading several frames
        for _ in range(5):  # Read and discard 5 frames
            self.cap.read()
        
        # Capture a frame from the camera
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame")
            return None

        # Crop the captured frame using the provided bounds
        cropped_frame = crop_frame(frame, self.X_BOUNDS, self.Y_BOUNDS)

        return cropped_frame

    def release(self):
        # Release the camera when done
        self.cap.release()
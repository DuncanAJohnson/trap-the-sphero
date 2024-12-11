from utils.crop_frame import crop_frame
import cv2

class Camera:
    def __init__(self, X_BOUNDS, Y_BOUNDS, camera_index=0):
        self.X_BOUNDS = X_BOUNDS
        self.Y_BOUNDS = Y_BOUNDS
        self.cap = cv2.VideoCapture(camera_index)

    def take_picture(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame")
            return None
        cropped_frame = crop_frame(frame, self.X_BOUNDS, self.Y_BOUNDS)
        return cropped_frame
    
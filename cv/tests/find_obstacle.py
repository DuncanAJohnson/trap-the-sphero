from cv.detect_obstacles import detect_obstacles
import cv2

# load the image
image = cv2.imread('images/4x3.jpg')
# detect the obstacles
obstacles = detect_obstacles(image)

print(obstacles)
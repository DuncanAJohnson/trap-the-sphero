from cv.detect_obstacles import detect_obstacles
import cv2

# load the image
image = cv2.imread('images/small_test.png')

# detect the obstacles
obstacles = detect_obstacles(image)

print(obstacles)
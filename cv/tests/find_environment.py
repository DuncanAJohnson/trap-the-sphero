from cv.detect_grid import detect_grid_squares
from cv.detect_obstacles import detect_obstacles
import cv2

# load the image
image = cv2.imread('images/small_test.png')

# detect the squares
squares = detect_grid_squares(image)

print("Grid centers: ", squares)

# detect the obstacles
obstacles = detect_obstacles(image)

print("Obstacle centers: ", obstacles)

# draw the centers on the frame
for center in squares:
    cv2.circle(image, center, 16, (0, 255, 0), -1)

for center in obstacles:
    cv2.circle(image, center, 16, (0, 0, 255), -1)

cv2.imshow('Image', image)
cv2.waitKey(0)

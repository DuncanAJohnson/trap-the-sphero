from cv.detect_grid import detect_grid_squares
from cv.detect_obstacles import detect_obstacles
import cv2

# load the image
image = cv2.imread('images/4x3_cropped.jpg')

# detect the grid
grid = detect_grid_squares(image)

print("Grid centers: ", grid)

# detect the obstacles
obstacles = detect_obstacles(image)

print("Obstacle centers: ", obstacles)

# draw the centers on the frame
for row in grid:
    for center in row:
        cv2.circle(image, center, 4, (0, 255, 0), -1)

for center in obstacles:
    cv2.circle(image, center, 4, (0, 0, 255), -1)

cv2.imshow('Image', image)
cv2.waitKey(0)

from cv.detect_grid import detect_grid_squares
import cv2

# load the image
image = cv2.imread('images/4x3.jpg')

# detect the squares
squares = detect_grid_squares(image)

print(squares)
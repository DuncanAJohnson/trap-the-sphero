import cv2
import numpy as np

def calculate_area(points):
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n  # Next vertex index
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2.0
    return area

def boxify_contour(contour):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    # calculate the area of the box
    center_x = int(np.mean(box[:, 0]))  # Average of x-coordinates
    center_y = int(np.mean(box[:, 1]))  # Average of y-coordinates
    center = (center_x, center_y)

    area = calculate_area(box)

    return box, area, center

# detects the squares in the image with a given color range and size range
def detect_squares(frame, color_range, size_range):

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    
    # mask out the color range
    mask = cv2.inRange(frame_hsv, color_range[0], color_range[1])

    # cv2.imshow('Masked', mask)
    # cv2.waitKey(0)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)

    # cv2.imshow('Blurred', blurred)
    # cv2.waitKey(0)

    # Perform edge detection using Canny
    edges = cv2.Canny(blurred, 90, 190, apertureSize=3)

    # cv2.imshow('Edges', edges)
    # cv2.waitKey(0)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # draw the contours on the frame
    contour_img = frame.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 3)

    # cv2.imshow('Contours', contour_img)
    # cv2.waitKey(0)

    centers = []

    for contour in contours:
        # Approximate the contour to a square
        box, area, center = boxify_contour(contour)

        # show the vertices on the frame
        img = frame.copy()
        for vertex in box:
            cv2.circle(img, tuple(map(int, vertex)), 4, (0, 0, 255), -1)

        # print(area)

        # cv2.imshow('Box', img)
        # cv2.waitKey(0)


        # Check if the square is the correct size to be a grid square
        if area > size_range[0] and area < size_range[1]:
            centers.append(center)

    return centers

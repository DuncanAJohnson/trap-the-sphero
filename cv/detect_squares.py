import cv2
import numpy as np

# Function to detect squares in a frame
def detect_squares(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (9, 9), 2)

    # Perform edge detection using Canny
    edges = cv2.Canny(gray, 90, 190, apertureSize=3)
    cv2.imshow('Edges', edges)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    contour_img = frame.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 3)
    cv2.imshow('Contours', contour_img)

    centers = []

    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        approx_img = frame.copy()
        cv2.drawContours(approx_img, approx, -1, (0, 255, 0), 3)
        cv2.imshow('Approx', approx_img)

        # Check if the polygon has 4 vertices (a square)
        if len(approx) >= 4 and len(approx) <= 7:
            # Calculate the center of the square
            M = cv2.moments(approx)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centers.append((cx, cy))

    return centers


# Open the video stream (0 for default camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the video stream
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if not ret:
        break

    # Detect squares in the frame
    squares = detect_squares(frame)

    for point in squares:
        point = (int(point[0]), int(point[1]))
        cv2.circle(frame, point, 4, (0, 255, 0), -1)

    # Display the frame with detected squares
    cv2.imshow('Squares Detected', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()
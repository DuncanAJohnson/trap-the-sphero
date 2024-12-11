import cv2
import numpy as np

def crop_frame(frame, x_bounds, y_bounds):
    """
    Crop an image given x and y bounds and save the result
    
    Args:
        frame (np.array): The input frame
        x_bounds (tuple): (x_min, x_max) coordinates for cropping
        y_bounds (tuple): (y_min, y_max) coordinates for cropping
    """
    # Extract bounds
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    
    # Ensure bounds are within image dimensions
    height, width = frame.shape[:2]
    x_min = max(0, x_min)
    x_max = min(width, x_max)
    y_min = max(0, y_min)
    y_max = min(height, y_max)
    
    # Crop the image
    cropped_img = frame[y_min:y_max, x_min:x_max]
    
    return cropped_img

# Example usage
if __name__ == "__main__":
    # Example parameters
    image_path = "images/4x3.jpg"
    
    output_path = "images/4x3_cropped.jpg"
    
    cropped = crop_image(image_path, x_bounds, y_bounds, output_path)

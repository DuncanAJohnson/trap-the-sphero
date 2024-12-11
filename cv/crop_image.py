import cv2
import numpy as np

def crop_image(image_path, x_bounds, y_bounds, output_path):
    """
    Crop an image given x and y bounds and save the result
    
    Args:
        image_path (str): Path to the input image
        x_bounds (tuple): (x_min, x_max) coordinates for cropping
        y_bounds (tuple): (y_min, y_max) coordinates for cropping
        output_path (str): Path where the cropped image will be saved
    """
    # Read the image
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError("Could not read the image")
    
    # Extract bounds
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    
    # Ensure bounds are within image dimensions
    height, width = img.shape[:2]
    x_min = max(0, x_min)
    x_max = min(width, x_max)
    y_min = max(0, y_min)
    y_max = min(height, y_max)
    
    # Crop the image
    cropped_img = img[y_min:y_max, x_min:x_max]
    
    # Save the cropped image
    cv2.imwrite(output_path, cropped_img)
    
    return cropped_img

# Example usage
if __name__ == "__main__":
    # Example parameters
    image_path = "images/4x3.jpg"
    x_bounds = (162, 379)
    y_bounds = (155, 392) 
    output_path = "images/4x3_cropped.jpg"
    
    cropped = crop_image(image_path, x_bounds, y_bounds, output_path)

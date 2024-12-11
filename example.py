from detect_sphero import WhiteRegionDetector
from move_sphero import SpheroController

if __name__ == "__main__":
    image_path = "my_photo-10.jpg"
    target_position = {"x": 400, "y": 200}

    center = WhiteRegionDetector.detect_largest_white_region(image_path)
    if center:
        print(f"Center coordinates of the largest white region: {center}")
        # controller = SpheroController(toy_name="SB-A644")
        # controller.move_to_target(center, target_position)

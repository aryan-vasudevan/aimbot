# Import libraries
import os
import time
import math
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient
import mss
import pyautogui
from PIL import Image

# Load environment variables
load_dotenv()

# Connect to the local inference server
client = InferenceHTTPClient(
    api_url=os.getenv("API_URL"),
    api_key=os.getenv("API_KEY")
)

# Configuration
SCREEN_WIDTH = 3440
SCREEN_HEIGHT = 1440
DETECTION_INTERVAL = 0.1  # Time between detections in seconds


def capture_screen():
    # Captures a screenshot of the entire screen
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        # Convert to PIL Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img


def box_center(prediction):
    # Returns the center point of a bounding box
    center_x = prediction['x']
    center_y = prediction['y']
    return (center_x, center_y)


def calculate_distance(point1, point2):
    # Calculates the Euclidean distance between two points
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


def find_closest_target(predictions, crosshair_position):
    # Finds the target closest to the crosshair
    if not predictions:
        return None

    closest_target = None
    min_distance = float('inf')

    for prediction in predictions:
        target_center = box_center(prediction)
        distance = calculate_distance(crosshair_position, target_center)

        if distance < min_distance:
            min_distance = distance
            closest_target = prediction

    return closest_target

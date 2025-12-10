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


def get_bounding_box_center(prediction):
    # Returns the center point of a bounding box
    center_x = prediction['x']
    center_y = prediction['y']
    return (center_x, center_y)

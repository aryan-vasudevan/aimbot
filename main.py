# Import libraries
import os
import time
import math
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient
import mss
from PIL import Image
import win32api
import win32con
from pynput import keyboard as pynput_keyboard

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
DETECTION_INTERVAL = 0.1

# Global flag for kill switch
running = True

def on_press(key):
    global running
    if hasattr(key, 'char') and key.char == 'p':
        print("\n[Stopping aimbot...]")
        running = False
        return False

listener = pynput_keyboard.Listener(on_press=on_press)
listener.start()


def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img


def box_center(prediction):
    return (prediction['x'], prediction['y'])


def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


def find_closest_target(predictions, crosshair_position):
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


def move_mouse_to_target(target_center):
    x = int(target_center[0])
    y = int(target_center[1])
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def run_detection(image):
    result = client.run_workflow(
        workspace_name=os.getenv("WORKSPACE_NAME"),
        workflow_id=os.getenv("WORKFLOW_ID"),
        images={"image": image},
        use_cache=False
    )
    if result and len(result) > 0:
        return result[0].get('predictions', {}).get('predictions', [])
    return []

print("Starting aimbot... Press P to stop.")

crosshair_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
print(f"Crosshair: {crosshair_position}")

while running:
    screenshot = capture_screen()
    predictions = run_detection(screenshot)

    if predictions:
        closest = find_closest_target(predictions, crosshair_position)
        if closest:
            target_center = box_center(closest)
            distance = calculate_distance(crosshair_position, target_center)
            print(f"Target: {target_center}, Distance: {distance:.0f}px, Confidence: {closest['confidence']:.0%}")
            move_mouse_to_target(target_center)

    time.sleep(DETECTION_INTERVAL)
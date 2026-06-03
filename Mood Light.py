from PIL import ImageGrab
import pyautogui
import numpy as np
import serial
import time

# --- Serial Config ---
SERIAL_PORT = 'COM3'    # Change this to your Arduino's port
BAUD_RATE = 9600

# --- Setup Serial ---
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Give Arduino time to reset

def get_pixel_color(x, y):
    # Capture a 1x1 image at mouse position
    img = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    rgb = img.getpixel((0, 0))
    return rgb

try:
    while True:
        # Get current mouse position
        x, y = pyautogui.position()

        # Get RGB color at that position
        r, g, b = get_pixel_color(x, y)

        # Send to Arduino
        msg = f"{r},{g},{b}\n"
        ser.write(msg.encode('utf-8'))

        time.sleep(0.1)  # Adjust update speed as needed

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    ser.close()

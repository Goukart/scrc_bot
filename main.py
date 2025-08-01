import sys
from os import register_at_fork

from Xlib.Xatom import WEIGHT
from pyautogui import *
import pyautogui
import time
from pynput.keyboard import Controller
import numpy as np
import random
from PIL import Image
from pyrect import WIDTH

# pyautogui is too slow? test with this
#from Xlib import X, display, ext
#d = display.Display()
#s = d.screen()
#root = s.root
#root.warp_pointer(300, 300)
#d.sync()

#Xlib.ext.xtest.fake_input(d, X.ButtonPress, 1)
#d.sync()
#time.sleep(0.001)
#Xlib.ext.xtest.fake_input(d, X.ButtonRelease, 1)
#d.sync()

SPACE_px: int = 79
FIRST_LANE_REL: int = 33
TRIGGER_LINE: int = 931

#ANHCOR is top left
ANCHOR_X: int = 808
ANCHOR_Y: int = 650
HEIGHT: int = 350
WIDTH: int = 304
SCREEN_REGION: tuple = (ANCHOR_X, ANCHOR_Y, HEIGHT, WIDTH)
TRIGGER_LINE_IN_CROP: int = TRIGGER_LINE - ANCHOR_Y - 25

# F
loc_f = Point(x=FIRST_LANE_REL, y=TRIGGER_LINE_IN_CROP)
# V
loc_v = Point(x=FIRST_LANE_REL + (SPACE_px * 1), y=TRIGGER_LINE_IN_CROP)
# ←
loc_l = Point(x=FIRST_LANE_REL + (SPACE_px * 2), y=TRIGGER_LINE_IN_CROP)
# ↓
loc_d = Point(x=FIRST_LANE_REL + (SPACE_px * 3), y=TRIGGER_LINE_IN_CROP)

# The interval between clicks
click_interval = 0.2

# Function to simulate a mouse click
def click_at(x, y):
    pyautogui.click(x, y)

# Simulate key combination Ctrl + C
#keyboard.press('ctrl')
#keyboard.press('c')
#keyboard.release('c')
#keyboard.release('ctrl')

def main():
    # Coordinates of the lanes
    button_coordinates = [loc_f, loc_v, loc_l, loc_d]

    #screenshot = pyautogui.screenshot(region=SCREEN_REGION).show()
    #screenshot.save("captured_screenshot.png")

    screen = Image.open("img.png").convert()
    array = np.array(screen)
    print(array.shape)

    crop = array[
           ANCHOR_Y:(ANCHOR_Y+HEIGHT),
           ANCHOR_X:(ANCHOR_X+WIDTH),
           :]

    print(TRIGGER_LINE_IN_CROP)
    print(crop.shape)
    crop[TRIGGER_LINE_IN_CROP, 0:] = [0,255,255]
    crop[TRIGGER_LINE_IN_CROP, loc_f.x] = [255, 0, 0]
    crop[TRIGGER_LINE_IN_CROP, loc_v.x] = [255, 0, 0]
    crop[TRIGGER_LINE_IN_CROP, loc_l.x] = [255, 0, 0]
    crop[TRIGGER_LINE_IN_CROP, loc_d.x] = [255, 0, 0]
    Image.fromarray(crop).save("crop.png")


    # Create a controller object
    keyboard = Controller()

    # click_at(800,600)

    # Type a string
    # keyboard.type('Hello, world!')

    # image = pyautogui.locateOnScreen('note_image.png')
    #if image:
    #    print("Found the note!")
    #    pyautogui.click(image)

    sys.exit()
    try:
        while True:
            for x, y in button_coordinates:
                click_at(x, y)  # Click on each button location
                time.sleep(click_interval)  # Wait for the next click
    except KeyboardInterrupt:
        print("Auto-clicker stopped.")

    # Get screen coordinates (for testing)
    #while True:
    #    sleep(0.2)
    #    print(pyautogui.position())

if __name__ == "__main__":
    main()
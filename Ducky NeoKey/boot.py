# -*- coding: utf-8 -*-
#############################################################
#                          IMPORTS                          #
#############################################################
import time
import board
import neopixel
from digitalio import DigitalInOut, Pull
import touchio
import storage

#############################################################
#                          CONTENT                          #
#############################################################
## NEOPIXEL
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
pixels.fill((0, 0, 0))

## BUTTON
button = DigitalInOut(board.SWITCH)
button.switch_to_input(pull=Pull.DOWN)

## TOUCH
touch = touchio.TouchIn(board.TOUCH)

if not button.value :
    storage.disable_usb_drive()
    pixels.fill((255, 0, 0))
    time.sleep(0.5)
else :
    pixels.fill((0, 255, 0))
    time.sleep(0.5)
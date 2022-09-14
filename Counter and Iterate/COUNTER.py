# -*- coding: utf-8 -*-
#############################################################
#                          IMPORTS                          #
#############################################################
import time
import board
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard

#________________________ US ________________________
# from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
# from adafruit_hid.keycode import Keycode  # pylint: disable=unused-import

#________________________ FR ________________________
from keyboard_layout_win_fr import KeyboardLayout
from keycode_win_fr import Keycode  # pylint: disable=unused-import

#____________________________________________________

from digitalio import DigitalInOut, Pull
import touchio

#############################################################
#                          CONTENT                          #
#############################################################
print("NeoKey Trinkey HID")
counter = 0

## NEOPIXEL
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
pixel.fill((255, 0, 255))

## KEYBOARD HID
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
#________________________ US ________________________
# keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

#________________________ FR ________________________
keyboard_layout = KeyboardLayout(keyboard)

#____________________________________________________

## BUTTON
# create the switch, add a pullup, start it with not being pressed
button = DigitalInOut(board.SWITCH)
button.switch_to_input(pull=Pull.DOWN)
button_state = False

## TOUCH
# create the captouch element and start it with not touched
touch = touchio.TouchIn(board.TOUCH)
touch_state = False

## THE REMOVE SEQUENCE
remove = (
   {'keys': Keycode.F2, 'delay': 0.2},
   {'keys': Keycode.HOME, 'delay': 0.1},
   {'keys': Keycode.DELETE, 'delay': 0.1},
   {'keys': Keycode.DELETE, 'delay': 0.1},
   {'keys': Keycode.DELETE, 'delay': 0.1},
   {'keys': Keycode.ENTER, 'delay': 0.1}
)

#############################################################
#                         FUNCTION                          #
#############################################################
def make_keystrokes(keys, delay):
    if isinstance(keys, str):  # If it's a string...
        keyboard_layout.write(keys)  # ...Print the string
    elif isinstance(keys, int):  # If its a single key
        keyboard.press(keys)  # "Press"...
        keyboard.release_all()  # ..."Release"!
    elif isinstance(keys, (list, tuple)):  # If its multiple keys
        keyboard.press(*keys)  # "Press"...
        keyboard.release_all()  # ..."Release"!
    time.sleep(delay)

#############################################################
#                         MAIN LOOP                         #
#############################################################
while True:
    if touch.value and not touch_state: 
        pixel.fill((0, 128, 255))
        touch_state = True
        print("touch")
        while touch.value :
            if button.value and not button_state:
                button_state = True

            if not button.value and button_state:
                counter += 1
                button_state = False

    sequence = ( ## Need to put this here otherwise index isn't updated
        {'keys': Keycode.F2, 'delay': 0.2},
        {'keys': Keycode.HOME, 'delay': 0.1},
        # {'keys': "{:02}X_\n".format(counter), 'delay': 0.1}
        {'keys': "{}X_\n".format(counter), 'delay': 0.1}
    )

    if not touch.value and touch_state:
        print("no touch")
        print(counter)
        touch_state = False
        if counter > 0 :
            for k in sequence:
                make_keystrokes(k['keys'], k['delay'])
        counter = 0
        pixel.fill((255, 0, 255))

    if button.value and not button_state:
        button_state = True

    if not button.value and button_state:
        for k in remove:
            make_keystrokes(k['keys'], k['delay'])
        button_state = False

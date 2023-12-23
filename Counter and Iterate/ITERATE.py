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
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode  # pylint: disable=unused-import

#________________________ FR ________________________
# from keyboard_layout_win_fr import KeyboardLayout
# from keycode_win_fr import Keycode  # pylint: disable=unused-import

#____________________________________________________

from digitalio import DigitalInOut, Pull
import touchio

print("NeoKey Trinkey HID")
index = 1
counter = 0

## NEOPIXEL
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
pixel.fill((255, 0, 255))

## KEYBOARD HID
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)

#________________________ US ________________________
keyboard_layout = KeyboardLayoutUS(keyboard)

#________________________ FR ________________________
# keyboard_layout = KeyboardLayout(keyboard)

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
sequence_2 = (
   {'keys': Keycode.F2, 'delay': 0.2},
   {'keys': Keycode.HOME, 'delay': 0.1},  # give it a moment to launch!
   {'keys': Keycode.DELETE, 'delay': 0.1},
   {'keys': Keycode.DELETE, 'delay': 0.1},
   {'keys': Keycode.DELETE, 'delay': 0.1},
   {'keys': Keycode.ENTER, 'delay': 0.1}
)

sequence_3 = [Keycode.ALT, Keycode.F4]

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
    sequence_1 = ( ## Need to put this here otherwise index isn't updated
        {'keys': Keycode.F2, 'delay': 0.2},
        {'keys': Keycode.HOME, 'delay': 0.1},  # give it a moment to launch!
        {'keys': "{:03}_\n".format(index), 'delay': 0.1}
    )

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

        if counter > 0 :
            print("Counter =  {}".format(counter))
            if counter == 1 :
                if isinstance(sequence_1, (list, tuple)) and isinstance(sequence_1[0], dict):
                    for k in sequence_1:
                        make_keystrokes(k['keys'], k['delay'])
                else:
                    make_keystrokes(sequence_1, delay=0)

                index += 1

            elif counter == 2 :
                if isinstance(sequence_2, (list, tuple)) and isinstance(sequence_2[0], dict):
                    for k in sequence_2:
                        make_keystrokes(k['keys'], k['delay'])
                else:
                    make_keystrokes(sequence_2, delay=0)

                if index <= 1 :
                    index = 1

                else :
                    index -= 1

            elif counter == 4 :
                make_keystrokes(sequence_3, delay=0)


    if not touch.value and touch_state:
        print("no touch")
        touch_state = False
        counter = 0
        pixel.fill((255, 0, 255))

    time.sleep(0.1)

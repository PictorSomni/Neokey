# -*- coding: utf-8 -*-
#############################################################
#                          IMPORTS                          #
#############################################################
import time
import board
import neopixel
import rainbowio
import usb_hid
from adafruit_hid.keyboard import Keyboard
# from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
# from adafruit_hid.keycode import Keycode  # pylint: disable=unused-import
from keyboard_layout_win_fr import KeyboardLayout
from keycode_win_fr import Keycode  # pylint: disable=unused-import
from digitalio import DigitalInOut, Pull
import touchio
import adafruit_ducky

#############################################################
#                          CONTENT                          #
#############################################################
print("NeoKey Trinkey HID")
counter = 0

## NEOPIXEL
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
pixels.fill((255, 0, 255))

## KEYBOARD HID
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
# keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)
keyboard_layout = KeyboardLayout(keyboard)

## BUTTON
# create the switch, add a pullup, start it with not being pressed
button = DigitalInOut(board.SWITCH)
button.switch_to_input(pull=Pull.DOWN)
button_state = False

## TOUCH
# create the captouch element and start it with not touched
touch = touchio.TouchIn(board.TOUCH)
touch_state = False

## DUCKY
duck = adafruit_ducky.Ducky("wifi_grabber.txt", keyboard, keyboard_layout)
yt = adafruit_ducky.Ducky("youtube.txt", keyboard, keyboard_layout)
result = True

## THE REMOVE SEQUENCE
remove = (
   {'keys': Keycode.F2, 'delay': 0.2},
   {'keys': Keycode.HOME, 'delay': 0.1},
   {'keys': Keycode.DELETE, 'delay': 0.1},
   {'keys': Keycode.DELETE, 'delay': 0.1},
   {'keys': Keycode.DELETE, 'delay': 0.1},
   {'keys': Keycode.ENTER, 'delay': 0.1}
)

close = [Keycode.ALT, Keycode.F4]

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


def wait(wait):
    now = time.monotonic()
    while (time.monotonic() - now) < wait :
        pixels.fill(rainbowio.colorwheel(int(time.monotonic() * 128) & 255))

def ducky(script) :
    result = True
    while result is not False:
        pixels.fill(rainbowio.colorwheel(int(time.monotonic() * 128) & 255))
        result = script.loop()

#############################################################
#                         MAIN LOOP                         #
#############################################################
while True:
    if touch.value and not touch_state: 
        pixels.fill((0, 128, 255))
        touch_state = True
        print("touch")
        while touch.value :
            if button.value and not button_state:
                button_state = True

            if not button.value and button_state:
                counter += 1
                button_state = False

    if not touch.value and touch_state:
        print("no touch")
        touch_state = False
        if counter > 0 :
            print("Counter =  {}".format(counter))
            if counter == 1 :
                ducky(duck)
            elif counter == 2 :
                ducky(yt)

        duck = adafruit_ducky.Ducky("wifi_grabber.txt", keyboard, keyboard_layout)
        yt = adafruit_ducky.Ducky("youtube.txt", keyboard, keyboard_layout)

        result = True
        counter = 0
        pixels.fill((255, 0, 255))

    if button.value and not button_state:
        button_state = True

    if not button.value and button_state:
        make_keystrokes(close, delay=0)
        button_state = False

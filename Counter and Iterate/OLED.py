# -*- coding: utf-8 -*-
#############################################################
#                          IMPORTS                          #
#############################################################
import random
import time
import board
import displayio
import terminalio
import digitalio
from adafruit_debouncer import Debouncer
import neopixel
import rainbowio
from adafruit_display_text import label
import adafruit_displayio_sh1107
import usb_hid
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_fr import KeyboardLayout
from keycode_win_fr import Keycode
# from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS


#############################################################
#                          CONTENT                          #
#############################################################
## CLEARS DISPLAY
displayio.release_displays()

## SETUP BUTTON PINS
pin_b = digitalio.DigitalInOut(board.D6)
pin_b.direction = digitalio.Direction.INPUT
pin_b.pull = digitalio.Pull.UP

pin_c = digitalio.DigitalInOut(board.D5)
pin_c.direction = digitalio.Direction.INPUT
pin_c.pull = digitalio.Pull.UP

## DEBOUNCE BUTTONS
button_b = Debouncer(pin_b) #6
button_c = Debouncer(pin_c) #5
button_b_state = False
button_c_state = False

## NEOPIXELS
pixels = neopixel.NeoPixel(board.D9, 2, brightness=0.1)
pixels.fill((0, 0, 0))

## I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

## KEYBOARD
time.sleep(1)
keyboard = Keyboard(usb_hid.devices)
# keyboard_layout = KeyboardLayoutUS(keyboard)
keyboard_layout = KeyboardLayout(keyboard)

## SH1107 OLED DISPLAY
WIDTH = 128
HEIGHT = 64

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

group = displayio.Group()
display.show(group)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

text = "STUDIO C"
text_area = label.Label(terminalio.FONT, text=text, scale=2, color=0xFFFFFF, x=18, y=30)
group.append(text_area)

index = 1
counter = 0

#############################################################
#                         SEQUENCES                         #
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

delete_sequence = (
    {'keys': Keycode.F2, 'delay': 0.3},
    {'keys': Keycode.HOME, 'delay': 0.1},
    {'keys': Keycode.DELETE, 'delay': 0.1},
    {'keys': Keycode.DELETE, 'delay': 0.1},
    {'keys': Keycode.DELETE, 'delay': 0.1},
    {'keys': Keycode.ENTER, 'delay': 0.1}
)

close_sequence = [Keycode.ALT, Keycode.F4]

## A BIT OF WAIT
time.sleep(0.5)

#############################################################
#                         MAIN LOOP                         #
#############################################################
while True :
    pixels.fill(rainbowio.colorwheel(int(time.monotonic() * 13) & 255))

    ## BOTH BUTTONS PRESSED
    if not pin_b.value and not pin_c.value :
        text_area.scale = 3
        text_area.x = 3
        text_area.y = 28
        text_area.text = "ANNULER"

        if isinstance(delete_sequence, (list, tuple)) and isinstance(delete_sequence[0], dict):
            for k in delete_sequence:
                make_keystrokes(k['keys'], k['delay'])
        else:
            make_keystrokes(delete_sequence, delay=0)

        if index <= 1 :
            index = 1
        else :
            index -= 1

        text_area.scale = 2
        text_area.x = 18
        text_area.y = 30
        text_area.text = "STUDIO C"

################################################

    ## LEFT BUTTON PRESSED AND MAINTAINED
    if not pin_c.value and not button_c_state: 
        pixels.fill((255, 0, 255))
        button_c_state = True

        text_area.scale = 2
        text_area.x = 6
        text_area.y = 30
        text_area.text = "CALENDRIER"

        while not pin_c.value :
            if not pin_b.value :
                counter += 1

    iterate_sequence = ( ## Need to put this here otherwise index isn't updated
        {'keys': Keycode.F2, 'delay': 0.3},
        {'keys': Keycode.HOME, 'delay': 0.1},
        {'keys': "{:02}_\n".format(index), 'delay': 0.1}
    )

    ## LEFT BUTTON RELEASED
    if pin_c.value and button_c_state:
        if counter > 0 :
            for k in iterate_sequence:
                make_keystrokes(k['keys'], k['delay'])
            index += 1

        text_area.scale = 2
        text_area.x = 18
        text_area.y = 30
        text_area.text = "STUDIO C"
        button_c_state = False
        counter = 0

################################################

    ## RIGHT BUTTON PRESSED AND MAINTAINED
    if not pin_b.value and not button_b_state: 
        pixels.fill((0, 85, 255))
        button_b_state = True

        text_area.scale = 2
        text_area.x = 4
        text_area.y = 30
        text_area.text = "IMPRESSION"
        while not pin_b.value :
            button_c.update()

            if button_c.fell  :
                counter += 1
                text_area.scale = 5

                if counter > 9:
                    text_area.x = 18
                else :
                    text_area.x = 36

                text_area.y = 25
                text_area.text = f"{counter}X"
                print(f"COUNTER = {counter}\n")

    counter_sequence = ( ## Need to put this here otherwise counter isn't updated
        {'keys': Keycode.F2, 'delay': 0.3},
        {'keys': Keycode.HOME, 'delay': 0.1},
        {'keys': "{}X_\n".format(counter), 'delay': 0.1}
    )

    ## RIGHT BUTTON RELEASED
    if pin_b.value and button_b_state:
        if counter > 0 :
            for k in counter_sequence:
                make_keystrokes(k['keys'], k['delay'])

        text_area.scale = 2
        text_area.x = 18
        text_area.y = 30
        text_area.text = "STUDIO C"
        button_b_state = False
        counter = 0

    ## A little pause so both buttons presses (for delete) is read a lot better
    time.sleep(0.2)
    display.show(group)

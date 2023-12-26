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

from adafruit_servokit import ServoKit

#############################################################
#                          CONSTANT                         #
#############################################################
DEFAULT_TEXT = "READY"
sequence = ["DUMMY", "SERVO", "CONTINUOUS"]
MAX = len(sequence) - 1
#############################################################
#                          FUNCTION                         #
#############################################################
def back_to_default ():
    text_area.scale = 2
    text_area.x = 36
    text_area.y = 30
    text_area.text = DEFAULT_TEXT

#############################################################
#                          CONTENT                          #
#############################################################
## SERVO
kit = ServoKit(channels=8)
kit.continuous_servo[7].set_pulse_width_range(550, 2500)

## CLEARS
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

## SH1107 OLED DISPLAY
WIDTH = 128
HEIGHT = 64

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

group = displayio.Group()
display.show(group)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

text = DEFAULT_TEXT
text_area = label.Label(terminalio.FONT)
back_to_default()
group.append(text_area)

## A BIT OF WAIT
time.sleep(0.5)

#############################################################
#                         MAIN LOOP                         #
#############################################################
counter = 0
while True :
    pixels.fill(rainbowio.colorwheel(int(time.monotonic() * 13) & 255))

    ## BOTH BUTTONS PRESSED
    if not pin_b.value and not pin_c.value :
        text_area.text = "RESET"

        kit.servo[0].angle = 90
        kit.servo[1].angle = 90
        time.sleep(1)
        
        back_to_default ()


################################################


    ## LEFT BUTTON PRESSED AND MAINTAINED
    if not pin_c.value and not button_c_state: 
        pixels.fill((255, 0, 255))
        button_c_state = True
        text_area.x = 6
        text_area.text = "180 turn ?"
        while not pin_c.value :
            button_b.update()

            if counter < MAX :
                if button_b.fell  :
                    counter += 1
                    text_area.x = 9
                    text_area.text = f"{sequence[counter]}"


    ## LEFT BUTTON RELEASED
    if pin_c.value and button_c_state:
        if counter > 0 :
            if counter == 1 :
                kit.servo[0].angle = 180
            else :
                kit.continuous_servo[7].throttle = 1
                time.sleep(2)
                kit.continuous_servo[7].throttle = 0
                time.sleep(0.5)

        back_to_default ()
        button_c_state = False
        counter = 0


################################################


    ## RIGHT BUTTON PRESSED AND MAINTAINED
    if not pin_b.value and not button_b_state: 
        pixels.fill((0, 85, 255))
        button_b_state = True
        text_area.x = 18
        text_area.text = "0 TURN ?"
        while not pin_b.value :
            button_c.update()

            if button_c.fell  :
                if counter < MAX :
                    counter += 1
                    text_area.x = 9
                    text_area.text = f"{sequence[counter]}"


    ## RIGHT BUTTON RELEASED
    if pin_b.value and button_b_state:
        if counter > 0 :
            if counter == 1 :
                kit.servo[0].angle = 0
            else :
                kit.continuous_servo[7].throttle = -1
                time.sleep(2)
                kit.continuous_servo[7].throttle = 0
                time.sleep(0.5)

        back_to_default ()
        button_b_state = False
        counter = 0

    ## A little pause so both buttons presses (for delete) is read a lot better
    time.sleep(0.2)
    display.show(group)

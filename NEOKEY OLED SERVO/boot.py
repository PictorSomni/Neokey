# -*- coding: utf-8 -*-
#############################################################
#                          IMPORTS                          #
#############################################################
import time
import board
import neopixel
import displayio
import terminalio
import digitalio
import digitalio
from adafruit_display_text import label
import adafruit_displayio_sh1107
import storage

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

text = ""
text_area = label.Label(terminalio.FONT, text=text, scale=2, color=0xFFFFFF, x=13, y=30)
group.append(text_area)

## BOTH BUTTONS PRESSED
if not pin_b.value and not pin_c.value :
    pixels.fill((255, 0, 0))
    text_area.x = 7
    text_area.text = "-< H@CK >-"
    
else :
    storage.disable_usb_drive()
    pixels.fill((0, 255, 0))
    text_area.text = "BONJOUR !"

time.sleep(0.5)

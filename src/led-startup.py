#!/usr/bin/python

import time
from dotstar import Adafruit_DotStar

numpixels = 60

#datapin = 23
#clockpin = 24
#strip = Adafruit_DotStar(numpixels, datapin, clockpin)

strip = Adafruit_DotStar(numpixels, 320000) # SPI (pins 10=MOSI(green), 11=SCLK(yellow))

strip.begin()
strip.setBrightness(64)
strip.clear()

white = 0xFFFFFF

for b in range(64):
    strip.setBrightness(b)
    for pixel in range(60):
       strip.setPixelColor(pixel, white)
    strip.show()
    time.sleep(0.015)

for pixel in range(60):
   strip.setPixelColor(pixel, white)

strip.show()

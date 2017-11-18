import time
from neopixel import *

COLOR_BLACK = Color(0, 0, 0)
COLOR_RED = Color(255, 0, 0)
COLOR_GREEN = Color(0, 255, 0)
COLOR_BLUE = Color(0, 0, 255)
COLOR_WHITE = Color(255, 255, 255)

class Matrix:

    def __init__(self, width, height):

        self.width = int(width)
        self.height = int(height)

        self.gpio_pin = 18
        self.freq_hz = 800000
        self.dma = 5
        self.invert = False
        self.brightness = 8
        self.channel = 0
        self.strip_type = ws.WS2812_STRIP


        self.strip = Adafruit_NeoPixel(self.width*self.height, self.gpio_pin, self.freq_hz, self.dma, self.invert, self.brightness, self.channel, self.strip_type)

    def clearStrip(self):
        return self.setStripColor(COLOR_BLACK)

    def setStripColor(self, color):
	"""Set entire strip to single color"""
        print "setting color " + str(color)
	for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        return self

    def test(self):
        self.strip.begin()
        self.clearStrip().strip.show()
        self.setStripColor(COLOR_RED).strip.show()
        time.sleep(1)
        self.setStripColor(COLOR_GREEN).strip.show()
        time.sleep(1)
        self.setStripColor(COLOR_BLUE).strip.show()
        time.sleep(1)
        self.setStripColor(COLOR_WHITE).strip.show()
        time.sleep(1)
        self.clearStrip().strip.show()

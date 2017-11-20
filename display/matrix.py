import time
from itertools import cycle
from neopixel import *
from spritesheet import rip_ascii_sprites

COLOR_BLACK = Color(0, 0, 0)
COLOR_RED = Color(255, 0, 0)
COLOR_GREEN = Color(0, 255, 0)
COLOR_BLUE = Color(0, 0, 255)
COLOR_WHITE = Color(255, 255, 255)

class Matrix:

    _matrix_map = []
    _ascii = []

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

        self.__createMatrixMap()
        self.__createAlphabet()
        
    def clearStrip(self):
        return self.setStripColor(COLOR_BLACK)

    def setStripColor(self, color):
	"""Set entire strip to single color"""
	for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        return self

    def drawStripes(self, colors):
        color_pool = cycle(colors)
        for y in range(self.height):
            color = next(color_pool)
            for x in range(self.width):
                self.strip.setPixelColor(self._matrix_map[y][x], color)
        return self

    def drawLetters(self):
        my_str = "ABCD"
        
        for y in range(8):
            x = 0
            for i in range(len(my_str)):
                #print i
                #print my_str
                #print my_str[i]
                #print ord(my_str[i])
                #print self._ascii
                img = self._ascii.get(ord(my_str[i]))
                for pixel in img[y]:
                    self.strip.setPixelColor(self._matrix_map[y][x], COLOR_BLUE if pixel else COLOR_BLACK)
                    x = x+1
        return self

    def test(self):
        self.strip.begin()
        self.clearStrip().strip.show()
        time.sleep(1)
        self.clearStrip().drawLetters().strip.show()
        time.sleep(5)
        self.setStripColor(COLOR_RED).strip.show()
        time.sleep(1)
        self.setStripColor(COLOR_GREEN).strip.show()
        time.sleep(1)
        self.setStripColor(COLOR_BLUE).strip.show()
        time.sleep(1)
        self.setStripColor(COLOR_WHITE).strip.show()
        time.sleep(1)
        #cycle through a list of colors
        colors = [COLOR_BLACK,COLOR_WHITE,COLOR_BLUE,COLOR_GREEN,COLOR_RED]
        #colors = [next(color_list) for i in range(5)]
        i = 0
        while i < 10:
            colors.insert(0, colors.pop())
            self.drawStripes(colors).strip.show()
            time.sleep(100/1000.0)
        self.clearStrip().strip.show()

    def __createMatrixMap(self):
        """
        form a mapping in a serpentine pattern zig-zagging top to bottom
        | |-| |
        | | | |
        |_| |_|
        """
        i = 0
        self._matrix_map = [[None for j in range(self.width) ] for n in range(self.height)]
        print "creating mmap"
        for x in range(self.width):
            for y in range(self.height):
                self._matrix_map[y if x % 2 == 0 else self.height-1-y][x] = i
                i = i + 1
        print "done"

    def __createAlphabet(self):
        self._ascii = rip_ascii_sprites("/home/pi/RetroPie-Custom/assets/glyphs/C64-font.bmp")
        print "alphabet done"

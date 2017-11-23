import time
from itertools import cycle
from neopixel import *
from spritesheet import rip_ascii_sprites
from mask import Mask
from surface import Surface
from rectangle import Rectangle

from animation import TextScroll

COLOR_BLACK = Color(0, 0, 0)
COLOR_RED = Color(255, 0, 0)
COLOR_GREEN = Color(0, 255, 0)
COLOR_BLUE = Color(0, 0, 255)
COLOR_YELLOW = Color(255,255,0)
COLOR_WHITE = Color(255, 255, 255)

class Matrix:

    _matrix_map = []
    _ascii = []
    _master_surface = None
    _master_mask = None

    def __init__(self, width, height):

        self.width = int(width)
        self.height = int(height)

        self.gpio_pin = 18
        self.freq_hz = 800000
        self.dma = 5
        self.invert = False
        self.brightness = 16
        self.channel = 0
        self.strip_type = ws.WS2812_STRIP

        self.strip = Adafruit_NeoPixel(self.width*self.height, self.gpio_pin, self.freq_hz, self.dma, self.invert, self.brightness, self.channel, self.strip_type)

        self.__createMatrixMap()
        #self.__createAlphabet()
        self.__createSurfaces()
        
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
                img = self._ascii.get(ord(my_str[i]))
                for pixel in img.pixels[y]:
                    self.strip.setPixelColor(self._matrix_map[y][x], COLOR_BLUE if pixel else COLOR_BLACK)
                    x = x+1
        return self

    def test(self):
        print "strip initializaiton"
        self.strip.begin()

        print "creating animation"
        anim = TextScroll("GO! GO! GO! GO! GO! GO! GO!")
        print "starting animation"
        for tick in anim.run(self._master_surface, 100):
            self.write().strip.show()
        self.clearStrip().strip.show()
        return
        print "write sleep 10"
        time.sleep(1)
        self.drawLetters().strip.show()
        time.sleep(1)
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

    def write(self):
        """dump the master matrix to the strip, using mask"""
        for y in range(self.height):
            for x in range(self.width):
                self.strip.setPixelColor(
                    self._matrix_map[y][x],
                    int(
                        self._master_surface.pixels[y][x] *
                        self._master_mask.pixels[y][x]
                    )
                )

        return self
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
        print "ripping alphabet sprites"
        self._ascii = rip_ascii_sprites("/home/pi/RetroPie-Custom/assets/glyphs/C64-font.bmp")

    def __createSurfaces(self):
        self._master_surface = Surface((self.width,self.height))
        self._master_surface.pixels.fill(COLOR_YELLOW)
        self._master_mask = Mask(self._master_surface.rect.size)
        self._master_mask.pixels[0][0] = 0
        self._master_mask.pixels[1][0] = 0
        self._master_mask.pixels[2][0] = 0
        self._master_mask.pixels[3][0] = 0
        self._master_mask.pixels[4][0] = 0
        self._master_mask.pixels[5][0] = 0
        self._master_mask.pixels[6][0] = 0
        self._master_mask.pixels[0][22] = 0
        self._master_mask.pixels[1][23] = 0
        self._master_mask.pixels[2][24] = 0
        self._master_mask.pixels[3][25] = 0
        self._master_mask.pixels[4][26] = 0
        self._master_mask.pixels[5][27] = 0
        self._master_mask.pixels[6][28] = 0        

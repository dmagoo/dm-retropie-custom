import scipy.misc
import numpy as np
from rectangle import Rectangle
from mask import Mask
from surface import Surface
from blit import blit

class spritesheet(object):
    def __init__(self, filename):
        self.sheet = Surface.fromArray(scipy.misc.imread(filename))
    def image_at(self, source_rect):
        """
        Loads image from x,y,x+offset,y+offset
        rectangle is defined as:
        x, y, width, height
        """
        image = Mask(source_rect.size)

        blit(image, self.sheet, source_rect=source_rect)

        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count):
        "Loads a strip of images and returns them as a list"
        rects = [Rectangle((rect.x+rect.width*x, rect.y, rect.width, rect.height))
                for x in range(image_count)]
        return self.images_at(rects)


def rip_ascii_sprites(spritesheet_path):
    ascii = {}

    ss = spritesheet(spritesheet_path)
    h = 8
    w = 8
    rows = 4

    img = []
    for row in range(rows):
        img = img + ss.load_strip(Rectangle((0,row*h,h,w)),32)


    #map ascii chars to image indexes
    #build a table of ascii codes to loaded image index
    for i in range(32,64):
        ascii[i] = img[i]

    ascii[8592] = img[31] # left arrow
    ascii[8593] = img[30] # up arrow
    ascii[93]   = img[29] # right bracket 
    ascii[156]  = img[28] # british pound
    ascii[91]   = img[27] # left bracket
    ascii[64]   = img[0]  # @

    #both lower and upper case letters are the same
    for i in range(1,27):
        ascii[64+i] = img[i]
        ascii[96+i] = img[i]

    return ascii

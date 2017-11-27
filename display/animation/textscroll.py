from copy import copy
from neopixel import *
from animation  import Animation
from ..surface import Surface
from ..mask import Mask
from ..rectangle import Rectangle
from ..spritesheet import rip_ascii_sprites
class TextScroll(Animation):
    text = None
    text_surface = None
    loop = False
    dx = -2
    dy = 0

    def __init__(self, text, viewport):
        self.text = str(text)
        #todo, move this to something more global
        print "ripping again - TODO, not this!"
        self._ascii = rip_ascii_sprites("/home/pi/RetroPie-Custom/assets/glyphs/C64-font.bmp")        
        print "setting up source surface+mask"
        self.text_surface = Surface((len(self.text)*8,8))
        tmp_mask = Mask((len(self.text)*8,8))        
        tmp_mask.pixels.fill(0)
        #give the surface some features so we can test maksing
        self.text_surface.pixels.fill(Color(30,30,0))
        self.text_surface.pixels[0] = [Color(40,0,50) for i in range(self.text_surface.rect.width)]
        self.text_surface.pixels[1] = [Color(40,0,40) for i in range(self.text_surface.rect.width)]
        self.text_surface.pixels[2] = [Color(35,10,30) for i in range(self.text_surface.rect.width)]
        self.text_surface.pixels[3] = [Color(35,10,20) for i in range(self.text_surface.rect.width)]
        self.text_surface.pixels[4] = [Color(30,20,10) for i in range(self.text_surface.rect.width)]
        self.text_surface.pixels[5] = [Color(30,20,5) for i in range(self.text_surface.rect.width)]
        self.text_surface.pixels[6] = [Color(30,30,0) for i in range(self.text_surface.rect.width)]
        self.text_surface.pixels[7] = [Color(30,30,0) for i in range(self.text_surface.rect.width)]
        print "mapping characters"
        
        left = 0 # all of our chars have the same width, but this method assumes they don't
        #map ascii mask onto master mask
        for i in range(len(text)):
            img = self._ascii.get(ord(text[i]))
            rect = Rectangle((left, 0, img.rect.width, img.rect.height))
            tmp_mask.blit(img, Rectangle((left, 0, img.rect.width, img.rect.height)))
            left += img.rect.width
        print "writing final source surface"
        self.text_surface.blit(self.text_surface,target_mask=tmp_mask)

        self.start_rect = copy(viewport)
        self.start_rect.x = viewport.width

        print "completing init"
        super( TextScroll, self ).__init__(
            self.text_surface,
            mask=None,
            target_rect=copy(self.start_rect),
            mask_clip=None
        )

    def onStart(self):
        print "starting scroll"

    def onEnd(self):
        print "ending scroll"

    def next(self):
        self.target_rect.x += self.dx
        self.target_rect.y += self.dy

        if self.loop:
            if (
                    self.dx > 0 and self.target_rect.x > self.surface.rect.width
            ) or (
                self.dx <= 0 and self.target_rect.x+self.surface.rect.width < 0
            ):
                self.target_rect.x = self.start_rect.x

            if (
                    self.dy > 0 and self.target_rect.y > self.surface.rect.height
            ) or (
                self.dy <= 0 and self.target_rect.y+self.surface.rect.height < 0
            ):
                self.target_rect.y = self.start_rect.y

        return True

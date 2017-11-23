from abc import ABCMeta
from neopixel import *
from ..mask import Mask

class Animation:
    __metaclass__ = ABCMeta

    ticks = 0
    additive = False # if true, do not clear surface between frames
    background_color = Color(0,0,0)
    
    def __init__(self, surface, mask=None, target_rect=None, mask_clip=None):

        self.target_rect = target_rect
        self.mask_clip = mask_clip
        self.surface = surface
        
        if mask is None:
            self.mask = Mask(surface.rect.size)

        if self.mask.rect.size != self.surface.rect.size:
            raise ValueError("mask shape must match surface shape")

    def run(self, target_surface, duration=None):
        self.onStart()

        while self._tick() and (duration is None or duration >= self.ticks):
            self.render(target_surface)
            yield self.ticks

        self.onEnd()
            
    def _tick(self):
        self.ticks += 1
        #print "tick %i" % (self.ticks)
        return self.next()

    def onStart(self):
        pass

    def onEnd(self):
        pass
    
    """ Return false when animation is done """
    def next(self):
        return True

    def render(self, target_surface):
        if not self.additive:
            target_surface.pixels.fill(self.background_color)

        try:
            target_surface.blit(self.surface,self.target_rect)
        except ValueError:
            #surface is off screen, and that's ok
            pass

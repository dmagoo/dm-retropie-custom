import numpy as np
from blit import blit
from rectangle import Rectangle

class Renderable:
    _init_value = 0
    def __init__(self, size):
        self.rect = Rectangle((0,0,size[0],size[1]))
        self.pixels = np.full((size[1],size[0]), self._init_value)
    
    def blit(self, source, target_rect=None, source_rect=None, target_mask=None):
        return blit(self, source, target_rect, source_rect, target_mask)

import numpy as np
from rectangle import Rectangle

class Renderable:
    _init_value = 0
    def __init__(self, size, viewport=None):
        if viewport is None:
            self.viewport = Rectangle((0,0,size[0],size[1]))
        else:
            self.viewport = viewport

        self.rect = Rectangle((0,0,size[0],size[1]))
        self.pixels = np.full((size[1],size[0]), self._init_value)
    
    #see blit.notes for sdl implementation
    def blit(source, dest):
        """ DOES NOT WORK WORK WITH NEGATIVE OFFSETS. PROBABLY HAS ISSUES W/ OVERLAPS
        dest could be a pair of x,y coordindates or a Rectangle. a rectangle imples clipping out areas
         beyond the width of the rectangle"""
        
        source_start_pos = source.rect.origin
        source_end_pos = [source.rect.x + source.rect.width-1,source.rect.y + source.rect.height-1]
        #so far, above does not take into account a smaller target
        
        dest_x, dest_y = dest.origin if isinstance(dest, Rectangle) else dest
        dest_width, dest_height = dest.size if isinstance(dest, Rectangle) else [self.rect.width-dest[0], self.rect.height-dest[1]]

        dest_width = min(dest_width, source.rect.width)
        dest_height = min(dest_height, source.rect.height)
        
        #does adjust for negatives yet
        target_start_pos = [dest_x, dest_y]
        target_end_pos = [
            dest_x+dest_width-1,
            dest_y+dest_height-1
        ]

	#np.set_printoptions(threshold='nan')
        """
        print  source[
        source_start_pos[1]:source_end_pos[1]+1,
        source_start_pos[0]:source_end_pos[0]+1
        ]
        """
        target[
            target_start_pos[1]:target_end_pos[1]+1,
            target_start_pos[0]:target_end_pos[0]+1
        ] = source[
            source_start_pos[1]:source_end_pos[1]+1,
            source_start_pos[0]:source_end_pos[0]+1
        ]

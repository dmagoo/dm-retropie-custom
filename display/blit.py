from copy import copy
import numpy as np
from rectangle import Rectangle

def blit(source, target, source_rect=None, target_rect=None):
    sr,tr = get_blit_maps(source, target, source_rect, target_rect)

    if None is sr:
        raise ValueError("Cannot map source to target")

    for y in range(sr.height):
        for x in range(sr.width):
            target.pixels[y+tr.y][x+tr.x] = source.pixels[y+sr.y][x+sr.x]

        x += 1
    y += 1

def get_blit_maps(source, target, source_rect=None, target_rect=None):
    """returns a rectangular window into source and target, highlighting where pixels align"""
    target_rect = copy(target.rect if target_rect is None else target_rect)

    #clip the source rectangle to the source surface
    if source_rect is not None:
        source_x = source_rect.x
        width = source_rect.width
        if source_x < 0:
            width += source_x
            target_rect.x -= source_x
            source_x = 0

        width = min(width, source.rect.width - source_x)

        source_y = source_rect.y
        height = source_rect.height
        if source_y < 0:
            height = height + source_y
            target_rect.y -= source_y
            source_y = 0

        height = min(height, source.rect.height - source_y)

    else:
        source_x = source_y = 0
        width = source.rect.width
        height = source.rect.height

    #clip the destination rectangle against the clip rectangle */
    clip_rect = target.rect

    dx = clip_rect.x - target_rect.x
    if dx > 0:
        width = width - dx;
        target_rect.x = target_rect.x + dx;
        source_x = source_x + dx;

    dx = target_rect.x + width - clip_rect.x - clip_rect.width;
    if dx > 0:
        width = width - dx

    dy = clip_rect.y - target_rect.y
    if dy > 0:
        height -= dy
        target_rect.y = target_rect.y + dy
        source_y = source_y + dy

    dy = target_rect.y + height - clip_rect.y - clip_rect.height;
    if dy > 0:
        height = height - dy

    if width > 0 and height > 0:
        target_rect.width = width
        target_rect.height = height
        sr = Rectangle((source_x, source_y, width, height))
        #return Rectangle((source_x, source_y, width, height))
        print "result: ",
        print ("%i,%i,%i,%i" % (sr.x, sr.y, sr.width, sr.height)),
        print " -> ",
        print ("%i,%i,%i,%i" % (target_rect.x, target_rect.y, target_rect.width, target_rect.height))
        print "===================="
        return [sr, target_rect]
	#return SDL_LowerBlit(source, sr, target, target_rect);
    return None
    #print "FALL THROUGH... error?"
        

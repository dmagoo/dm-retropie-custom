from copy import copy
import numpy as np
from rectangle import Rectangle

def blit(target, source, target_rect=None, source_rect=None, target_mask=None):
    sr,tr = get_blit_maps(target, source, target_rect, source_rect)

    if target_mask is not None and target_mask.rect.size != target.rect.size:
        raise ValueError("Target mask dimensions must match target dimensions")

    value_matrix = source.pixels[
        sr.y:sr.y+sr.height,
        sr.x:sr.x+sr.width
    ]

    if target_mask is not None:
        value_matrix = np.multiply(value_matrix, target_mask.pixels)

    target.pixels[
        tr.y:tr.y+tr.height,
        tr.x:tr.x+tr.width
    ] = value_matrix

    """
    old way. about 10 times slower
    for y in range(sr.height):
        for x in range(sr.width):
                target.pixels[y+tr.y][x+tr.x] = source.pixels[y+sr.y][x+sr.x] * (target_mask.pixels[y+tr.y][x+tr.x] if target_mask is not None else 1)
        x += 1
    y += 1
    """

def get_blit_maps(target, source, target_rect=None, source_rect=None):
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
        #print "result: ",
        #print ("%i,%i,%i,%i" % (sr.x, sr.y, sr.width, sr.height)),
        #print " -> ",
        #print ("%i,%i,%i,%i" % (target_rect.x, target_rect.y, target_rect.width, target_rect.height))
        #print "===================="
        return [sr, target_rect]

    raise ValueError("Cannot map source to target")

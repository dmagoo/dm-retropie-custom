from copy import deepcopy
import numpy as np
from display.surface import Surface
from display.rectangle import Rectangle
from display.blit import blit


def print_surface(surface):
    for y in surface.pixels:
        for x in y:
            print int(x),
        print "\n"

print "testing"
target = Surface((10,5))
source = Surface((3,8))

print "target"
target.pixels = np.full((5,10), 0)
print_surface(target)

print "source"

#source.pixels = np.full((8,3), 1)
a = range(24)
source.pixels = np.reshape(a, (8,3))
print_surface(source)

for r in [
        [Rectangle((0,0,3,5)), None, "source-rect in bounds, no target specified"],
        [Rectangle((0,0,10,3)), None, "source-rect out of bounds, no target specified"],
        [Rectangle((0,0,1,1)), Rectangle((0,0,2,2)), "target rect larger"],
        [Rectangle((0,0,3,3)), None, "small source square, no target rect"],
        [Rectangle((1,1,2,2)), Rectangle((3,3,5,2)), "source rect fine, too big for target rect"],
        [None, Rectangle((-1,-1,3,5)), "small source square, no target rect, offset negative on target"],
        [Rectangle((-1,-1,3,8)), None, "small source square, no target rect, offset negative on source"]
]:
    print "=================="
    print r[2]
    print "passing in: ",
    rect = source.rect if r[0] is None else r[0]
    print ("%i,%i,%i,%i" % (rect.x, rect.y, rect.width, rect.height)),
    print " -> ",
    rect = target.rect if r[1] is None else r[1]
    print ("%i,%i,%i,%i" % (rect.x, rect.y, rect.width, rect.height))
    target_copy = deepcopy(target)
    blit(source, target_copy, r[0], r[1])
    print "||||||||||| OUTPUT ||||||||||||"
    print_surface(target_copy)

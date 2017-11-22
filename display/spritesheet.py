import scipy.misc
import numpy as np

def blit(source, target, source_rect, target_rect):
    """ DOES NOT WORK WORK WITH NEGATIVE OFFSETS. PROBABLY HAS ISSUES W/ OVERLAPS   """

    source_start_pos = source_rect[0:2]
    source_end_pos = [source_rect[0] + source_rect[2]-1,source_rect[1] + source_rect[3]-1]

    target_start_pos = [i if i >= 0 else 0 for i in target_rect[0:2]]
    target_end_pos = [target_rect[i]+target_rect[i+2]-1 if (target_rect[i]+target_rect[i+2]-1) < target.shape[i] else target.shape[i]-1 for i in [0,1]]

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

class spritesheet(object):

    def __init__(self, filename):
        self.sheet = scipy.misc.imread(filename)
            
    def image_at(self, rectangle):
        """
        Loads image from x,y,x+offset,y+offset
        rectangle is defined as:
        x, y, width, height
        """
        image = np.zeros((rectangle[2], rectangle[3]))

        blit(self.sheet, image, rectangle, (0, 0, rectangle[2], rectangle[3]))
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups)


def rip_ascii_sprites(spritesheet_path):
    ascii = {}

    ss = spritesheet(spritesheet_path)
    h = 8
    w = 8
    rows = 4

    img = []
    for row in range(rows):
        img = img + ss.load_strip((0,row*h,h,w),32)


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

from renderable import Renderable

class Mask(Renderable):
    _init_value = 1
    @staticmethod
    def fromArray(np_array):
        ret = Mask(list(reversed(np_array.shape)))
        ret.pixels = np_array
        return ret

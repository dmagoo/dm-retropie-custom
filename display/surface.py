from renderable import Renderable

class Surface(Renderable):
    @staticmethod
    def fromArray(np_array):
        ret = Surface(list(reversed(np_array.shape)))
        ret.pixels = np_array
        return ret





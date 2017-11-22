from renderable import Renderable

class Surface(Renderable):
    @staticmethod
    def fromArray(np_array):
        ret = Surface(np_array.shape)
        ret.pixels = np_array
        return ret





class Rectangle:

    def __init__(self, geometry):
        self.x, self.y, self.width, self.height = geometry

    def _getSize(self):
        return (self.width, self.height)

    def _getOrigin(self):
        return (self.x, self.y)

    size = property(_getSize)

    origin = property(_getOrigin)

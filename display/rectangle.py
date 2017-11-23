class Rectangle:

    def __init__(self, geometry):
        self.x, self.y, self.width, self.height = geometry

    def _getSize(self):
        return (self.width, self.height)
    size = property(_getSize)
    
    def _getOrigin(self):
        return (self.x, self.y)
    origin = property(_getOrigin)

    def __str__(self):
        return "(%i,%i) %ix%i" % (self.x, self.y, self.width, self.height)

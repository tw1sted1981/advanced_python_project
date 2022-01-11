#******************************************************************************
# content       = Point class
#               Should probably switch to inheriting from np.ndarray
#               when I am more familiar with numpy as research suggests
#               this is a good thing to do.
#                 
#
# date          = 2022-01-10
#
# dependencies  = 
# todos         =
#
# author        = Chris Forrester <chrisforrester.tv@gmail.com>
#******************************************************************************

class Point():
    """
    Class to represent a point in cartesian coordinates.  Origin (0,0) assumed to be 
    top left corner ie same as opencv.

    include convenience functions to switch origin to bottom left corner like nuke
    """
    def __init__(self, x, y, width=1920, height=1080):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def point(self):
        return self.x, self.y

    def status(self):
        print('point position ({},{}) on a plane of {}x{}'.format(self.x, self.y, self.width, self.height))

    def point_in_nuke(self):
        """ 0,0 top left converted to 0,0 bottom left"""
        return self.x, self.height - self.y 


if __name__ == '__main__':
    a = Point(20,20,100,100)
    a.status()
    print(a.point())
    print(a.width)

    print(a.point_in_nuke())
    print(a.point_in_nuke()[0])



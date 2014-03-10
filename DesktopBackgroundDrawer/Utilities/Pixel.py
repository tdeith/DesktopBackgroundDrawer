'''
Created on Mar 7, 2014

@author: tdeith
'''

from Colours import Colour

class Pixel(object):
    '''
    The pixel class is used to represent a single pixel, with accessors to the neighbours of that pixel, 
    the pixel's colour, and pixel's location.  
    '''

    def __init__(self, x = 0, y = 0, colour = Colour(), neighbours=[]):
        self.X, self.Y = x,y
        self.Colour = colour
        self.Neighbours = neighbours
        self.QueueIndex = -1
        
    
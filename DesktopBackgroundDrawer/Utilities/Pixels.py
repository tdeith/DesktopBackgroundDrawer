'''
Created on Mar 25, 2014

@author: tdeith
'''

from Pixel import Pixel
from Colour import Colour

class PixelList(list):
    '''
    This class represents a collection of pixels, and contains useful methods
    for storing/accessing/modifying said pixels.
    '''


    def __init__(self, width, height):
        
        '''
        Constructor
        '''
        
        # Set up the base list
        list.__init__(self)
        
        # Create the width x height pixel array
        for x in xrange(width):
            for y in xrange(height):
                self[x][y] = Pixel(x, y)
                
        # Initialize the list of completed pixels             
        self.CompletedPixels = [[False for x in xrange(width)] for x in xrange(height)]
        self.PixelQueue = []
        self.Width = width
        self.Height = height
        
    def UpdateNeighbours(self, x, y):
        if (self.Width > x + 1 and self.Height > y + 1):
            
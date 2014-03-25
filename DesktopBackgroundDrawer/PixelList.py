'''
Created on Mar 25, 2014

@author: tdeith
'''

from Pixel import Pixel
from Colour import Colour #@UnusedImport
from collections import deque

class PixelList(object):
    '''
    This class represents a collection of pixels, and contains useful methods
    for storing/accessing/modifying said pixels.
    '''


    def __init__(self, width, height):
        
        '''
        Constructor
        '''        
        # Create the width*height pixel array
        self._pixels = [[Pixel(x,y)for x in xrange(width) ] for y in xrange(height)]
                
        # Initialize the list of which pixels are yet to be touched
        self.UntouchedPixels = [[True for x in xrange(width)] for x in xrange(height)]
        self.PixelQueue = deque()
        self.Width = width
        self.Height = height
        
        
    def UpdateNeighbours(self, x, y):
        
        # Get the colour the neighbouring pixels will be updated with
        newColour = self[x][y].Colour
        
        # Loop through the immediately neighbouring pixel coordinates
        for (newx, newy) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            
            # Check that this pixel is in range
            if (self.Width -1 > newx and 
                self.Height - 1 > newy and 
                0 <= newx and
                0 <= newy):
                
                # Update the target colour of this neighbouring pixel
                self[newx][newy].UpdateTarget(newColour)
                
                # Add this new neighbour to the queue, if it hasn't already been addressed. 
                if (self.UntouchedPixels[newx][newy]):
                    self.UntouchedPixels[newx][newy]
                    self.PixelQueue.append((newx,newy))
                    
    def NextPixel(self):
        if ( 0 < len(self.PixelQueue)):
            # For FIFO behaviour, use popleft here. For LIFO behaviour, use pop.
            (x,y) = self.PixelQueue.popleft()
            yield self[x][y]
            
    def __getitem__(self, index):
        return self._pixels[index]
        
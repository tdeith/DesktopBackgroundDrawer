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
        self._pixels = [[Pixel(x,y)for y in xrange(height) ] for x in xrange(width)]
                
        # Initialize the list of which pixels are yet to be touched
        self.UntouchedPixels = [[True for y in xrange(height)] for x in xrange(width)]
        self.PixelQueue = deque()
        self.Width = width
        self.Height = height
        
        
    def __getitem__(self, index):
        '''
        Let's allow interfacing as though this is actually a list...
        '''
        return self._pixels[index]        
        
    def UpdateNeighbours(self, x, y):
        '''
        Called to update all neighbours in the vicinity of a pixel; each neighbouring
        pixel will have it's target (ideal) colour updated, and will be added to the 
        processing queue if it hasn't yet been added.
        '''
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
                    self.UntouchedPixels[newx][newy] = False
                    self.PixelQueue.append((newx,newy))
                    
    def NextPixel(self):
        '''
        Pop the next pixel from the processing queue
        '''
        while ( 0 < len(self.PixelQueue)):
            # For FIFO behaviour, use popleft here. For LIFO behaviour, use pop.
            (x,y) = self.PixelQueue.popleft()
            yield self[x][y]
                
    def FlatRows(self):
        '''
        Generate rows of pixels, formatted to be flat (1-D) lists 
        (i.e, [0,0,0, 0,0,0, 0,0,0] instead of 
              [(0,0,0),(0,0,0),(0,0,0)] )
        '''
        for row in list(zip(*self)):
            RGBRow = []
            for pixel in row:
                RGBRow.extend((pixel.Colour.R, pixel.Colour.G, pixel.Colour.B))
            yield RGBRow
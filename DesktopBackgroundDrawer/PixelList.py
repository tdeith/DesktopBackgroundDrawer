'''
Created on Mar 25, 2014

@author: tdeith
'''

from Pixel import Pixel
from Colour import Colour #@UnusedImport
from collections import deque
import random

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
        self._pixels = [[Pixel(x,y) for y in xrange(height) ] for x in xrange(width)]
                
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
        
        CentralPixel = self[x][y]
        
        # Make sure this pixel doesn't get processed again
        self.UntouchedPixels[x][y] = False
                
        # Loop through the immediately neighbouring pixel coordinates
        for (newx, newy) in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            
            # Check that this pixel is in range
            if (self.Width > newx and 
                self.Height > newy and 
                0 <= newx and
                0 <= newy):
                
                self[newx][newy].UpdateTarget(CentralPixel .Colour)

                # Add this new neighbour to the queue if it hasn't already been addressed. 
                if (self.UntouchedPixels[newx][newy]):
                    self.UntouchedPixels[newx][newy] = False
                    
                    # Update the target colour of this neighbouring pixel
                    self.PixelQueue.append((newx,newy))
                    
    def NextPixel(self):
        '''
        Pop the next pixel from the processing queue
        '''
    
        while ( 0 < len(self.PixelQueue)):
            nextIndex = random.randint(0,len(self.PixelQueue)-1)
            # For FIFO behaviour, use popleft here. For LIFO behaviour, use pop. For somewhat-behaviour, do this randint stuff...

            (x,y) = self.PixelQueue[nextIndex]
            del self.PixelQueue[nextIndex]
            
            # (x,y) = self.PixelQueue.popleft()
            
            assert ( self[x][y].X == x )
            assert ( self[x][y].Y == y )
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
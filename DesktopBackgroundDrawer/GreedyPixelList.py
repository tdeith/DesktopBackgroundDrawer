'''
Created on Mar 25, 2014

@author: tdeith
'''

from collections import deque
from PixelList import PixelList
import random

class GreedyPixelList(PixelList):
    '''
    This class represents a collection of pixels, where each pixel is queued for 
    greedily picking a colour from the list of colours yet to be assigned.
    '''


    def __init__(self, width, height):
        '''
        Standard constructor
        '''
        
        # Make me a new PixelList
        PixelList.__init__(self, width, height, 4)
        
        # Initialize the list of which pixels are yet to have chosen a colour
        self.UntouchedPixels = [[True for y in xrange(height)] for x in xrange(width)]      # @UnusedVariable
        
        # Create the queue of pixels to be processed
        self.PixelQueue = deque()
        
        # Assign the methods used for fetching pixel neighbours, updating pixel colours, and 
        #    fetching the next pixel in the queue.
        self.NeighbourListGenerator = self.NeighbourCoordinateGeneratorNarrow
        self.UpdatePixelTarget = self.UpdatePixelByAverage
        self.NextPixel = self.RandomNextPixelInQueue
        

    def NeighbourCoordinateGeneratorNarrow(self, x, y):
        '''
        Yield the 4 immediately adjacent pixels
        '''
        for newx,newy in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            yield (newx, newy)
                              
    def NeighbourCoordinateGeneratorBroad(self, x, y):
        '''
        Yield neighbouring pixels in a 5x5 square around the central pixel
        '''
        for newx, newy in ((x+dx,y+dy) for dy in range(-2,2) for dx in range(-2,2)):
            if (x != newx and y != newy): 
                yield (newx,newy)
    
    def UpdateNeighbours(self, x=-1, y=-1):
        '''
        Called to update all neighbours in the vicinity of a pixel; each neighbouring
        pixel will have it's target (ideal) colour updated, and will be added to the 
        processing queue if it hasn't yet been added.
        '''
        
        # If this function is being called without x,y arguments, then a pixel must have
        #   been fetched from the pixel queue. If not, something's gone awry. 
        if (x == -1 and y == -1):
            try:
                x,y=self._lastPoppedPixelCoords
            except (AttributeError) :
                print "Exception: UpdateNeighbours was called for the first time without identifying the \
first coordinates to update from."
                raise
                
        
        # Make sure this pixel doesn't get processed again
        self.UntouchedPixels[x][y] = False
                
        # Loop through the neighbouring pixel coordinates
        for (newx, newy) in self.NeighbourListGenerator(x,y):
            
            # Check that this pixel is in range, and hasn't already been processed
            if (self.Width > newx and 
                self.Height > newy and 
                0 <= newx and
                0 <= newy and
                self[newx][newy][3] != -1):
                                    
                # Update the target colour of this neighbouring pixel
                self.UpdatePixelTarget(newx, newy, x, y)

                # Add this new neighbour to the queue if it hasn't already been queued. 
                if (self.UntouchedPixels[newx][newy]):
                    self.UntouchedPixels[newx][newy] = False
                    self.PixelQueue.append((newx,newy))
                    
    def UpdatePixelByAverage(self, updateX, updateY, controllingX, controllingY):
        
        R, G, B, NeighbourCounter = self[updateX][updateY]
        
        newR, newG, newB = self[controllingX][controllingY][0:3]
        
        if (NeighbourCounter == -1):
            # This pixel has already selected a colour; we don't want to edit its target
            return
        elif (NeighbourCounter == 0 ):
            # This is the first neighbour this pixel has found
            R,G,B = newR, newG, newB
        else:  
            # Update this pixel's R,G,B values to 
            R = float(R * NeighbourCounter + newR)/(NeighbourCounter + 1)
            G = float(G * NeighbourCounter + newG)/(NeighbourCounter + 1)
            B = float(B * NeighbourCounter + newB)/(NeighbourCounter + 1)
            
    
        NeighbourCounter += 1
        
        self[updateX][updateY] = [R,G,B,NeighbourCounter]
                    
    def RandomNextPixelInQueue(self):
        '''
        Yield a random pixel in the queue for processing
        '''
        while ( 0 < len(self.PixelQueue)):
            nextIndex = random.randint(0,len(self.PixelQueue)-1)
            
            # Retrieve and un-"queue" this pixel
            x,y = self.PixelQueue[nextIndex]
            del self.PixelQueue[nextIndex]
            
            self._lastPoppedPixelCoords = (x,y)
            yield self[x][y]
            
    def FirstNeighbourInQueue(self):
        '''
        Yield the first neighbour in the queue for processing
        '''
        while ( 0 < len(self.PixelQueue)):
            (x,y) = self.PixelQueue.popleft()
            self._lastPoppedPixelCoords = (x,y)
            yield self[x][y]
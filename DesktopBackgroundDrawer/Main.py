'''
Created on Mar 10, 2014

@author: tdeith
'''

from Colours import *
from Pixel import *
from PixelQueue import *

if __name__ == '__main__':
    
    # StartTime = now
    
    # Initialize the list of colours to be placed
    
    # Insert one pixel from the list to the image in a random spot - place in PixelQueue
    
    ''' Logic 1: Requires that PixelQueue is a set or list!!!!
    
    PixelsCompleted = {} -- Will be a dict of (x,y) tuples. Hopefully it makes checking new pixels for uniqueness fast.
     
    Sort each colour (by Hue? Sat?) 
    
    For each colour in list
        BestSuitability = big
        
        For each pixel in queue
           CurrentSuitability = some function of RGB values               O(1)
           If CurrentSuitability < BestSuitability                        O(1)
           IdealPixel = pixel                                             O(1)
        pixel.colour = colour
        pixelQueue.remove(pixel)                                          O(p)
        
        pixel.UpdateNeighbours                                            O(p)
        PixelsCompleted[(pixel.x,pixel.y)]=pixel
            
            
    O(p*n) = O(n^1.5)   :    n ~= p^2
    Memory: big list of colours 
    '''
    
    '''Logic 2: 
    
    While PixelQueue is not empty
        for each colour in list
    
    '''
    return
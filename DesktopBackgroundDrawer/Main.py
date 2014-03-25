'''
Created on Mar 10, 2014

@author: tdeith
'''

from Colour import *            # @UnusedWildImport
from Pixel import *             # @UnusedWildImport
from PixelList import *         # @UnusedWildImport
from datetime import datetime
from random import randint

if __name__ == '__main__':
    
    # StartTime = now
    StartTime = datetime.now()
    
    
    # Set resolution, set number of bits, check that number of bits is big enough for resolution
    colourBits = 6
    width = 512
    height = 512
    
    assert (width * height <= 2**(colourBits * 3))

    # Initialize the list of colours to be placed
    # TODO: Make this a better data structure for finding best neighbours. Please. Please.
    
    ColoursUsedTable = [[[False for n in xrange(2**colourBits)]\
                                for n in xrange(2**colourBits)]\
                                for n in xrange(2**colourBits)]
    
    # Insert one pixel from the list to the image in a random spot - place neighbours in PixelQueue
    image = PixelList(width, height)
    
    (RandR, RandG, RandB) = (randint(0,2**colourBits-1),
                             randint(0,2**colourBits-1),
                             randint(0,2**colourBits-1))
    
    image[randint(0,width-1)][randint(0,height-1)].Colour = Colour(RandR, RandG, RandB)
    
    ''' Logic 1: Requires that PixelQueue is a set or list!!!!
    
    PixelsCompleted = [][] -- Will be a list'o'lists measuring X*Y
     
    Sort each colour (by Hue? Sat?)                                       O(nlogn)
    
    For each colour in list                                               O(n)
        BestSuitability = big
        
        For each pixel in queue                                           O(p)
           CurrentSuitability = some function of RGB values               
           If ( CurrentSuitability < BestSuitability ||
               (CurrentSuitability == BestSuitability &&
                SomeOtherFactorMakesThisPixelPreferedOverTheOtherOne)):
               IdealPixel = pixel                                         
        pixelQueue.remove(IdealPixel)                                     O(p)
        IdealPixel.colour = colour
        
        pixel.UpdateNeighbours                                            O(p)
        PixelsCompleted[pixel.x][pixel.y]=IdealPixel
        
            
    O(p*n) = O(n^1.5)   :    n ~= p^2
    Memory: big list of colours (2,000,000*3*8 bits ~= 6-12MB), PixelsCompleted gets big (2,000,000 x (2x12bit for x,y, 8bit for colour reference) = 8-16MB) - probably from 14-28MB
    
                Since this approach favours placing colours at the ideal pixel, it should get a very organic-growth-like spread of the pixels,
                where the spread occurs in whatever order the colours are sorted. This could make some very neat patterns.
    
    '''
    
    '''
    While PixelQueue is not empty
        BestSuitability = big
        
        for each colour in list                                            O(n)
            CurrentSuitability = some function of RGB values
           CurrentSuitability = some function of RGB values               
           If ( CurrentSuitability < BestSuitability ||
               (CurrentSuitability == BestSuitability &&
                SomeOtherFactorMakesThisPixelPreferedOverTheOtherOne)):
               IdealPixel = pixel                                         
        colourList.remove(IdealColour)                                     O(p)
        Pixel.Colour = IdealColour
        
        Pixels.AddNeighbours(x,y)
    '''
    print "Done!"
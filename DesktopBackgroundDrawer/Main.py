'''
Created on Mar 10, 2014

@author: tdeith
'''

from Colour import *            # @UnusedWildImport
from Pixel import *             # @UnusedWildImport
from PixelList import *         # @UnusedWildImport
from datetime import datetime
from random import randint
from xmlrpclib import MAXINT
import png

if __name__ == '__main__':
    
    # StartTime = now
    StartTime = datetime.now()
    
    
    # Set resolution, set number of bits, check that number of bits is big enough for resolution
    colourBits = 4
    width = 64  
    height = 64
    
    assert (width * height <= 2**(colourBits * 3))
    
    print "a", datetime.now() - StartTime

    # Initialize the list of colours to be placed
    # TODO: Make this a better data structure for finding best neighbours. Please. Please.
    
    ColoursUsedTable = [[[False for n in xrange(2**colourBits)]\
                                for n in xrange(2**colourBits)]\
                                for n in xrange(2**colourBits)]
    
    print "b", datetime.now() - StartTime
    
    # Insert one pixel from the list to the image in a random spot - place neighbours in PixelQueue
    image = PixelList(width, height)
    
    (RandR, RandG, RandB) = (random.randint(0, 2**colourBits-1),
                             random.randint(0, 2**colourBits-1),
                             random.randint(0, 2**colourBits-1))
    
    print "c", datetime.now() - StartTime
    
    (startx, starty) = (randint(0,width-1),randint(0,height-1))
    
    print startx, starty, RandR, RandG, RandB
    
    image[startx][starty].Colour = Colour(RandR, RandG, RandB)
    image.UpdateNeighbours(image[startx][starty])
    ColoursUsedTable[RandR][RandG][RandB] = True
    
    print "d", datetime.now() - StartTime
    
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
    
    i = 1
    
    for pixel in image.NextPixel():
        lookRange = 2 + int(2**colourBits*float(i/(width*height)))
        IdealColour = None
        BestSuitability = MAXINT
        for R in range(int(max([0,pixel.TargetColour.R-lookRange])),int(min([2**colourBits-1,pixel.TargetColour.R+lookRange]))):
            if ([entry for entries in ColoursUsedTable[R] for entry in entries].count(False) == 0):continue
            for G in range(int(max(0,pixel.TargetColour.G-lookRange)),int(min([2**colourBits-1,pixel.TargetColour.G+lookRange]))):
                if (ColoursUsedTable[R][G].count(False) == 0):continue
                for B in range(int(max([0,pixel.TargetColour.B-lookRange])),int(min([2**colourBits-1,pixel.TargetColour.B+lookRange]))):
                    if (ColoursUsedTable[R][G][B]):continue
                    CurrentSuitability = pixel.TargetColour.GetCartesianDist((R,G,B))
                    if ((CurrentSuitability < BestSuitability) or
                        ((CurrentSuitability == BestSuitability) and
                         (pixel.TargetColour.GetHueDist((R,G,B)) < pixel.TargetColour.GetHueDist((IdealColour.R,IdealColour.G,IdealColour.B))))):
                        BestSuitability = CurrentSuitability
                        IdealColour = Colour(R,G,B)
        try:
            ColoursUsedTable[IdealColour.R][IdealColour.G][IdealColour.B] = True
        except:
            print "Colour error on pixel", i , ". look range is", lookRange
            raise        
        
        pixel.Colour=IdealColour
        image.UpdateNeighbours(pixel)
        i += 1
        if (i%1000 == 0):png.from_array(image.FlatRows(), "RGB", {"height":height,"bitdepth":colourBits}).save("C:/temp/generate.png")
    

    png.from_array(image.FlatRows(), "RGB", {"height":height,"bitdepth":colourBits}).save("C:/temp/generate.png")
    
    print "Done! I took", datetime.now() - StartTime
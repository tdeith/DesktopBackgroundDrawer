'''
Created on Mar 10, 2014

@author: tdeith
'''

from Colour import *            # @UnusedWildImport
from Pixel import *             # @UnusedWildImport
from PixelList import *         # @UnusedWildImport
from ColourSpace import *       # @UnusedWildImport
from datetime import datetime
from random import randint
import png

if __name__ == '__main__':
    
    # StartTime = now
    StartTime = datetime.now()
    
    
    # Set resolution, set number of bits, check that number of bits is big enough for resolution
    colourBits = 7
    width = 1024
    height = 2048
    
    assert (width * height <= 2**(colourBits * 3))
    
    print "a", datetime.now() - StartTime
    
    print "b", datetime.now() - StartTime
    
    # Insert one pixel from the list to the image in a random spot - place neighbours in PixelQueue
    image = PixelList(width, height)
    for x in xrange(1):
        RandR, RandG, RandB = (random.randint(0, 2**colourBits-1),
                               random.randint(0, 2**colourBits-1),
                               random.randint(0, 2**colourBits-1))
        
        print "c", datetime.now() - StartTime
        
        startx, starty = (randint(0,width-1),randint(0,height-1))
        
        print startx, starty, RandR, RandG, RandB
        
        image[startx][starty].Colour = Colour(RandR, RandG, RandB)
        
        image.UpdateNeighbours(startx,starty)
        
        colourTable = ColourSpace(colourBits)
        colourTable.FlagColourAsUsed(RandR, RandG, RandB)
    
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
    
    assert([x for x in colourTable._searchSpace for x in x for x in x].count(0)>0)
    
    for pixel in image.NextPixel():
        NearbyColours = colourTable.GetNearestNeighbours(pixel.TargetColour.R, pixel.TargetColour.G, pixel.TargetColour.B)
        
        assert(NearbyColours is not None)
        if(len(NearbyColours) <= 0):
            print "aaarg! ",
            pixel.printTarget()
            print [x for x in colourTable._searchSpace for x in x for x in x].count(-1)
            png.from_array(image.FlatRows(), "RGB", {"height":height,"bitdepth":colourBits}).save("C:/temp/generate.png")
            raise Exception("Aaaerg!") 


        BestMatch = None
        for CurrentColour in NearbyColours:
            if ( BestMatch is None ):
                BestMatch = CurrentColour
            if ( pixel.TargetColour.GetHueDist(CurrentColour) < \
                 pixel.TargetColour.GetHueDist(BestMatch)):
                BestMatch = CurrentColour
            
        pixel.Colour = Colour(RGB = BestMatch)
        colourTable.FlagColourAsUsed(RGB=BestMatch)
        
        image.UpdateNeighbours(pixel.X, pixel.Y)
        i += 1
        if (i%1000 == 0):
            print i
        if (i%10000 == 0):
            png.from_array(image.FlatRows(), "RGB", {"height":height,"bitdepth":colourBits}).save("C:/temp/generate%(number)i.png" % {"number":i/10000})
    

    png.from_array(image.FlatRows(), "RGB", {"height":height,"bitdepth":colourBits}).save("C:/temp/generate.png")
    
    print [x for x in colourTable._searchSpace for x in x for x in x].count(-1)
    
    print "Done! I took", datetime.now() - StartTime
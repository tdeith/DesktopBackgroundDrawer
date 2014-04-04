'''
Created on Mar 10, 2014

@author: tdeith
'''

from GreedyPixelList import *               # @UnusedWildImport
from SearchableColourSpace import *         # @UnusedWildImport
from SearchablePixelSpace import *          # @UnusedWildImport
from ColourUtilities import GetHue, GetHueDist, GetSat
from datetime import datetime
from random import randint
import png
import cProfile
import threading

def MakeImage(image, height, colourBits, FileName):
    png.from_array(image.FlatRows(), "RGB", {"height":height,"bitdepth":colourBits}).save(FileName)


def GetColoursForGreedyPixels():    
    # Make a new searchable colour space
    colourSpace = SearchableColourSpace(colourBits)

    # Insert one pixel from the list to the image in a random spot - place neighbours in PixelQueue
    image = GreedyPixelList(width, height)
    
    RandR, RandG, RandB = (random.randint(0, 2**colourBits-1),
                           random.randint(0, 2**colourBits-1),
                           random.randint(0, 2**colourBits-1))
        
    startx, starty = (randint(0,width-1),randint(0,height-1))
    
    image[startx][starty] = (RandR, RandG, RandB, -1)
    
    image.UpdateNeighbours(startx,starty)
    
    colourSpace.FlagColourAsUsed(RandR, RandG, RandB)
        
    i = 1
    
    for pixel in image.NextPixel():
        NearbyColours = colourSpace.GetNearestNeighbours(pixel[0:3])
        
        assert(NearbyColours is not None)
        if(len(NearbyColours) <= 0):
            print "aaarg! ",
            pixel.printTarget()
            print [x for x in colourSpace._searchSpace for x in x for x in x].count(-1)
            png.from_array(image.FlatRows(), "RGB", {"height":height,"bitdepth":colourBits}).save("C:/temp/generate.png")
            raise Exception("Aaaerg!") 


        BestMatch = None
        for CurrentColour in NearbyColours:
            if ( BestMatch is None ):
                BestMatch = CurrentColour
            if  (GetHueDist(pixel[0:3], CurrentColour) < \
                 GetHueDist(pixel[0:3], BestMatch)):
                BestMatch = CurrentColour
            
        pixel[3] = -1
        pixel[0:3] = BestMatch
        
        colourSpace.FlagColourAsUsed(RGB=BestMatch)
        
        image.UpdateNeighbours()
        i += 1
        if (i%10000 == 0):
            print i, datetime.now()- StartTime
        if (i%imageInterval == 0):
            MakeImageThread = threading.Thread(target = MakeImage, args=(image, height, colourBits, "C:/temp/3360/generate%(number)i.png" % {"number":i/imageInterval}))
            MakeImageThread.start()
    

    MakeImage(image, height, colourBits, "C:/temp/3360/generate.png")

def GetPixelsForGreedyColours():
    # Make a new searchable pixels space
    print "Making the pixel table and eating your memory"
    pixelSpace = SearchablePixelSpace(width, height, colourBits)
    
    # Make the big sorted list of colours 
    startx, starty = (randint(0,width-1),randint(0,height-1))
   
    colourSort = lambda x,y:cmp(GetHue(x), GetHue(y))
    
    print "Making and sorting the list of all available colours. This may take a while."

    colourQueue = deque((sorted([[R,G,B] 
                                 for B in xrange(2**colourBits) 
                                 for G in xrange(2**colourBits)
                                 for R in xrange(2**colourBits)], 
                              colourSort)))
                              
    '''
    
    colourQueue = deque([[R,G,B] 
                        for B in xrange(2**colourBits) 
                        for G in xrange(2**colourBits)
                        for R in xrange(2**colourBits)])

    random.shuffle(colourQueue)
    '''    
    print "Rotating some colours around."
    randRotateIndex = random.randint(0,2**(3*colourBits)-1)
    colourQueue.rotate(randRotateIndex)
    
    
        
    RandR, RandG, RandB =  colourQueue.popleft()
        
    print RandR, RandG, RandB 
    
    pixelSpace[startx][starty] = (RandR, RandG, RandB, -1)
    pixelSpace.UpdateNeighbours(startx, starty)
    
    i = 1
    
    print "Giving colours a pixel to call home..."
    
    while( len(colourQueue) > 0):
        R,G,B = colourQueue.popleft()
        bestPixel = pixelSpace.GetBestPixelForColour((R,G,B))
        pixelSpace.MarkPixelAsTaken((R, G, B), bestPixel)
        pixelSpace.UpdateNeighbours(bestPixel[3], bestPixel[4])
 
        if (i%1000 == 0):
            print i, datetime.now()- StartTime
        if (i%imageInterval == 0):
            MakeImageThread = threading.Thread(target = MakeImage, args=(pixelSpace, height, colourBits, "C:/temp/2generate.png"))
            MakeImageThread.start()
        i += 1
        
    MakeImage(pixelSpace, height, colourBits, "C:/temp/2generate.png")

def TimeMe():
    StartTime = datetime.now()
    
    # Set resolution, set number of bits, check that number of bits is big enough for resolution
    colourBits = 4
    width = 64
    height = 64
    imageInterval = width*height/4
    OutputFileName = "C:/temp/3360/generate.png"
    
    assert (width * height <= 2**(colourBits * 3))
    
    GetPixelsForGreedyColours()
    
    print "Done! I took", datetime.now() - StartTime

if __name__ == '__main__':

    StartTime = datetime.now()
    
    colourBits = 4
    width = 64
    height = 64
    imageInterval = width*height/4
    OutputFileName = "C:/temp/3360/generate.png"

    
    cProfile.run("TimeMe()")
    

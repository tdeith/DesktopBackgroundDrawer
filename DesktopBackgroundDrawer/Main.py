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

    
def SteppedSortedColourList():
    allColours = [(R,G,B)
                    for B in xrange(2**colourBits) 
                    for G in xrange(2**colourBits)
                    for R in xrange(2**colourBits)]
    lowSatColours = []
    highSatColours = []
    for colour in allColours:
        if ( GetSat(colour, colourBits) > 0.15):
            highSatColours.append(colour)
        else:
            lowSatColours.append(colour)
    highSatColours = deque(sorted(highSatColours, 
                                  lambda RGB1,RGB2 : cmp(GetHue(RGB1), GetHue(RGB2))))
    rotateIndex = random.randint(0,len(highSatColours)-1)
    
    random.shuffle(lowSatColours)
    highSatColours.rotate(rotateIndex)
    highSatColours.append(deque(lowSatColours))
    assert len(highSatColours) == len(allColours)
    return highSatColours

def SortedColourList():
    allColours = deque(sorted(
                        [(R,G,B) for B in xrange(2**colourBits) 
                                 for G in xrange(2**colourBits)
                                 for R in xrange(2**colourBits)],
                       lambda RGB1,RGB2 : cmp(GetHue(RGB1), GetHue(RGB2))))

    rotateIndex = random.randint(0,2**colourBits-1)
    
    allColours.rotate(rotateIndex)
    return allColours

def RandomColourList():
    allColours = [(R,G,B)
                    for B in xrange(2**colourBits) 
                    for G in xrange(2**colourBits)
                    for R in xrange(2**colourBits)]
    
    random.shuffle(allColours)
    return deque(allColours)

def SortedDivergingColourList():
    randomHue = randint(0,360)
    allColours = deque(sorted(
                        [(R,G,B) for B in xrange(2**colourBits) 
                                 for G in xrange(2**colourBits)
                                 for R in xrange(2**colourBits)],
                        
                        lambda RGB1,RGB2 : cmp(abs(randomHue - GetHue(RGB1)), 
                                              abs(randomHue - GetHue(RGB2)))))
    return allColours

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
        
    print "Making the list of colours to be used up"
    colourQueue = SortedDivergingColourList()
    
    firstR, firstG, firstB =  colourQueue.popleft()
        
    print firstR, firstG, firstB 
    
    pixelSpace[startx][starty] = (firstR, firstG, firstB, -1)
    pixelSpace.UpdateNeighbours(startx, starty)
    
    i = 1
    
    print "Giving colours a pixel to call home..."
    
    while( len(colourQueue) > 0):
        R,G,B = colourQueue.popleft()
        bestPixel = pixelSpace.GetBestPixelForColour((R,G,B), i)
        if (not bestPixel):
            break
        pixelSpace.MarkPixelAsTaken((R, G, B), bestPixel)
        pixelSpace.UpdateNeighbours(bestPixel[3], bestPixel[4], i)
 
        if (i%10000 == 0):
            print i, datetime.now()- StartTime
        if (i%imageInterval == 0):
            MakeImageThread = threading.Thread(target = MakeImage, args=(pixelSpace, height, colourBits, "C:/temp/2generate"+str(i/imageInterval)+".png"))
            MakeImageThread.start()
        i += 1
        
    MakeImage(pixelSpace, height, colourBits, "C:/temp/2generate.png")
    
def TimeMe():

    GetPixelsForGreedyColours()
    
if __name__ == '__main__':

    StartTime = datetime.now()
    
    colourBits = 8
    width = 1050
    height = 3320
    imageInterval = width*height/128
    OutputFileName = "C:/temp/3360/generate.png"
    cProfile.run("TimeMe()")
    GetPixelsForGreedyColours()

    print "Done! I took", datetime.now() - StartTime

    

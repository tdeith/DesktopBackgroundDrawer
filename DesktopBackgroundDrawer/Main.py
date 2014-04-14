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

def SteppedSatSortedHueColourList():
    allColours = [(R,G,B)
                    for B in xrange(2**colourBits) 
                    for G in xrange(2**colourBits)
                    for R in xrange(2**colourBits)] * colourReuse
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

def IsInHueRangePredicate(minHue, maxHue):
    if minHue < maxHue:
        return lambda x: ((x < maxHue) and (x >= minHue))
    if minHue > maxHue:
        return lambda x: ((x < maxHue) or (x >= minHue))
    if minHue == maxHue: 
        return lambda x: True
        

def SortedHueColourList():
    startingHue = random.randint(0,360)
    hueIterations = max(1, int((colourReuse * 2**(3*colourBits))/(2**21)))
    hueWalkDistance = 360.0 / hueIterations
    minHue = startingHue
    maxHue = ( startingHue + hueWalkDistance ) % 360.0
    for i in xrange(hueIterations):
        print "\nMaking the list of which colours will be used next. (List iteration " + str(i+1) + ")..."
        isInRange = IsInHueRangePredicate(minHue, maxHue)
        colourSelection = deque(sorted([(R,G,B) 
                                  for B in xrange(2**colourBits) 
                                  for G in xrange(2**colourBits)
                                  for R in xrange(2**colourBits)
                                  if (isInRange(GetHue((R,G,B))))]* colourReuse,
                           lambda RGB1,RGB2 : cmp(GetHue(RGB1), GetHue(RGB2))))
        if hueIterations == 1:
            colourSelection.rotate(randint(0,len(colourSelection)-1))
        print "    Done."
        for colour in colourSelection: 
            yield colour
        minHue = maxHue
        maxHue = ( maxHue + hueWalkDistance ) % 360.0

def RandomColourList():
    allColours = [(R,G,B)
                    for B in xrange(2**colourBits) 
                    for G in xrange(2**colourBits)
                    for R in xrange(2**colourBits)] * colourReuse
    
    random.shuffle(allColours)
    return deque(allColours)

def SortedDivergingHueColourList():
    startingHue = random.randint(0,360)
    hueIterations = max(1, int((colourReuse * 2**(3*colourBits))/(2**18)))
    hueWalkDistance = 180.0 / hueIterations
    minHueDiff = 0
    maxHueDiff = ( startingHue + hueWalkDistance ) % 180.0
    for i in xrange(hueIterations):
        print "\nMaking the list of which colours will be used next. (List iteration " + str(i+1) + ")..."
        colourSelection = sorted([(R,G,B) 
                                for B in xrange(2**colourBits) 
                                for G in xrange(2**colourBits)
                                for R in xrange(2**colourBits)
                                if ((GetHueDist((R,G,B), None, startingHue) < maxHueDiff) and
                                    (GetHueDist((R,G,B), None, startingHue) >= minHueDiff))] * colourReuse,
                            lambda RGB1,RGB2 : cmp(abs(startingHue - GetHue(RGB1)), 
                                                   abs(startingHue - GetHue(RGB2))))
        print "    Done."
        for colour in colourSelection:
            yield colour
        minHueDiff = maxHueDiff
        maxHueDiff = ( maxHueDiff + hueWalkDistance ) % 180.0
            

def GetColoursForGreedyPixels():    
    # Make a new searchable colour space
    colourSpace = SearchableColourSpace(colourBits, colourReuse)

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
            png.from_array(image.FlatRows(), "RGB", {"height":height,"bitdepth":colourBits}).save(fileName+".png")
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
            MakeImageThread = threading.Thread(target = MakeImage, args=(image, height, colourBits, fileName+"_"+str(i/imageInterval)+".png"))
            MakeImageThread.start()
    

    MakeImage(image, height, colourBits, fileName+".png")

def GetPixelsForGreedyColours():
    # Make a new searchable pixels space
    print "\nInitializing the list of pixels, and eating your memory..."
    pixelSpace = SearchablePixelSpace(width, height, colourBits)
    print "    Done."

    # Make the big sorted list of colours 
    startx, starty = (randint(0,width-1),randint(0,height-1))
        
    colourQueue = SortedHueColourList()
    
    firstR, firstG, firstB =  colourQueue.next()
        
    pixelSpace[startx][starty] = (firstR, firstG, firstB, -1)
    pixelSpace.UpdateNeighbours(startx, starty)
    
    i = 1
    
    print "\nGiving colours a pixel to call home..."
    
    for R,G,B in colourQueue:
        bestPixel = pixelSpace.GetBestPixelForColour((R,G,B), (startx,starty), i)
        if (not bestPixel):
            break
        pixelSpace.MarkPixelAsTaken((R, G, B), bestPixel)
        pixelSpace.UpdateNeighbours(bestPixel[3], bestPixel[4], i)
 
        if (i%10000 == 0):
            print "    "+str(i/1000)+"k pixels finished. ", datetime.now()- StartTime, "elapsed." 
        if (i%imageInterval == 0):
            MakeImageThread = threading.Thread(target = MakeImage, args=(pixelSpace, height, colourBits, fileName+"_"+str(i/imageInterval)+".png"))
            MakeImageThread.start()
        i += 1
        
    pixelSpace.OnFinishedSearching()
        
    MakeImage(pixelSpace, height, colourBits, fileName+".png")
    print "Done! This all took", datetime.now() - StartTime

    
def TimeMe():

    GetPixelsForGreedyColours()
    
if __name__ == '__main__':

    StartTime = datetime.now()
    
    colourBits = 8
    colourReuse = 1
    width = 1050
    height = 3360
    imageInterval = width*height/1
    fileName = "D:/temp/"+str(width)+"x"+str(height)

    assert (width * height <= colourReuse * 2**(3*colourBits))

    cProfile.run("TimeMe()")

    

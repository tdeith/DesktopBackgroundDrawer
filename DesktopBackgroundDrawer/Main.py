'''
Created on Mar 10, 2014

@author: tdeith
'''

from GreedyPixelList import *               # @UnusedWildImport
from SearchableColourSpace import *         # @UnusedWildImport
from SearchablePixelSpace import *          # @UnusedWildImport
from datetime import datetime
from random import randint
import ColourLists
import png
import cProfile
import threading

def MakeImage(image, height, colourBits, FileName):
    png.from_array(image.FlatRows(), "RGB", {"height":height,"bitdepth":colourBits}).save(FileName)

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
        if (i%1000 == 0):
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
        
    colourQueue = ColourLists.SortedHueColourList(colourBits, colourReuse)
    
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

def GetPixelsAndColoursForEachother():
    print "\nInitializing the lists of pixels and colours, and eating your memory..."
    pixelSpace = SearchablePixelSpace(width, height, colourBits)


    
def TimeMe():

    GetPixelsForGreedyColours()
    
if __name__ == '__main__':

    StartTime = datetime.now()
    
    colourBits = 4
    colourReuse = 1
    width = 64
    height = 64
    imageInterval = width*height/1
    fileName = "C:/temp/"+str(width)+"x"+str(height)

    assert (width * height <= colourReuse * 2**(3*colourBits))

    cProfile.run("TimeMe()")

    

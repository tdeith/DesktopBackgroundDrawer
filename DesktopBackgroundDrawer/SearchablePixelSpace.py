'''
Created on Apr 3, 2014

@author: tdeith
'''

from PixelList import PixelList
from ColourBucket import ColourBucket, AddColour, RemoveColour, UpdateColour
from ColourUtilities import GetHueDist
from xmlrpclib import MAXINT
from math import sqrt
import random

class SearchablePixelSpace(PixelList):
    '''
    Holds a list of pixels which has been optimized for nearest-neighbour searches of 
    which pixel contains an ideal target colour in the 3-D colour space 
    '''
    
    def __init__(self, width, height, colourBits):
        '''
        Constructor
        '''
        PixelList.__init__(self, width, height, 5)

        # Initialize the methods we'll use for pixel neighbour grabbing etc
        self.NeighbourListGenerator = CircularNeighbourGenerator(3)
                
        # n, (Where 2**n is the size of our smallest buckets
        self.BucketDim = max(colourBits-6, 1)
        
        # The number of bits being used for colour data
        self.ColourBits = colourBits
        
        # The width of the colour space
        self.ColourWidth = 2**(self.ColourBits)
        
        # The number of small buckets along an edge of the colour space
        self.BucketWidth = 2**(self.ColourBits - self.BucketDim)

        # Create the buckets of colours and corresponding pixels
        self.ColourBucket = ColourBucket(2**(colourBits-1), 2**(colourBits-1), 2**(colourBits-1), 
                                         colourBits, self.BucketDim)
        
        self.AvailablePixels = set(())
        
    def MakeCandidateList(self,(targetR,targetG,targetB)):
        currentBestRadius = MAXINT
        bucketList = []
        candidateColours = []
                
        bucketList.append(self.ColourBucket)
        while ( bucketList ):
            currentCandidate = bucketList.pop()
            if currentCandidate.HasChildren:
                for child in currentCandidate.Children:
                    dist = sqrt((targetR-child.MidR)**2+
                                (targetG-child.MidG)**2+
                                (targetB-child.MidB)**2)
                    if (dist <= currentBestRadius):
                        bucketList.extend(currentCandidate.Children)
                        if (currentBestRadius > dist + 2**child.Size):
                            currentBestRadius = dist + 2**child.Size
                        
            else:
                candidateColours.extend(currentCandidate.Children)
            # end if
        #end while
        return candidateColours

        
    def GetBestPixelForColour(self, (targetR,targetG,targetB), intervalCount):
        candidateList = self.MakeCandidateList((targetR, targetG, targetB))
       
        ''' # Buckets - specifically walking through them
        else:
            for ShellList in self.ExpandingBucketShellList((targetR, targetG, targetB)):
                for RGB in ShellList:
                    candidate = self.ColourBucket.GetBucketNearest(RGB)
                    if candidate.Population > 0:
                        for colour in candidate.Colours:
                            candidateList.append(colour)
                if len(candidateList) > 0: 
                    break                
                        # end for
                    # end if
                # end for 
            #end while
        '''

        # Find the best candidate amongst the candidates we just fetched from the buckets
        currentBestRadius = MAXINT
        currentBestCandidate = []
        
        random.shuffle(candidateList)
        
        for (R,G,B,x,y,intervalAdded) in candidateList:
            distToTarget = (sqrt((targetR - R)**2 +
                                 (targetG - G)**2 + 
                                 (targetB - B)**2) -
                            (intervalCount - intervalAdded))
            if ( distToTarget < currentBestRadius or
                (distToTarget == currentBestRadius and
                  GetHueDist((targetR,targetG,targetB), (R,G,B)) <
                  GetHueDist((targetR,targetG,targetB), currentBestCandidate[0:3]))):
         
                # This colour is, so far, closer in distance, or equal in distance and closer in 
                #   hue, to the target colour.
                currentBestCandidate = [R,G,B,x,y,intervalAdded]
                currentBestRadius = distToTarget
        
        return currentBestCandidate
        
    def MarkPixelAsTaken(self, (newR, newG, newB),(R,G,B,x,y,intervalAdded)):
        RemoveColour(self.ColourBucket, (R,G,B,x,y,intervalAdded))
        self[x][y] = [newR, newG, newB, -1]
        
    def UpdateNeighbours(self, x=-1, y=-1, intervalCount = 1):
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
                                
        # Loop through the neighbouring pixel coordinates
        for (newx, newy, canAdd) in self.NeighbourListGenerator(x,y):
            
            # Check that this pixel is in range, and hasn't already been processed
            if (self.Width > newx and 
                self.Height > newy and 
                0 <= newx and
                0 <= newy and
                self[newx][newy][3] != -1):
                                    
                # Update the target colour of this neighbouring pixel
                self.UpdatePixelTarget(newx, newy, x, y, canAdd*intervalCount)

    def UpdatePixelTarget(self, updateX, updateY, controllingX, controllingY, intervalCount):
        
        oldR, oldG, oldB, NeighbourCounter, intervalAdded = self[updateX][updateY]
        
        controlR, controlG, controlB = self[controllingX][controllingY][0:3]
        
        if (NeighbourCounter == -1):
            # This pixel has already selected a colour; we don't want to edit its target
            return
        elif ( NeighbourCounter == 0 ):
            # This is the first neighbour this pixel has found
            newR, newG, newB = controlR, controlG, controlB
        else:  
            # Update this pixel's R,G,B values to 
            newR = float(oldR * NeighbourCounter + controlR)/(NeighbourCounter + 1)
            newG = float(oldG * NeighbourCounter + controlG)/(NeighbourCounter + 1)
            newB = float(oldB * NeighbourCounter + controlB)/(NeighbourCounter + 1)
            
       
        NeighbourCounter += 1
                    
        if ( intervalCount and not intervalAdded):
            AddColour(self.ColourBucket, (newR, newG, newB, updateX, updateY, intervalCount))
            self[updateX][updateY] = [newR,newG,newB,NeighbourCounter, intervalCount] 
        elif (intervalAdded):
            UpdateColour(self.ColourBucket, (oldR, oldG, oldB, newR, newG, newB, updateX, updateY, intervalAdded))
            self[updateX][updateY] = [newR,newG,newB,NeighbourCounter, intervalAdded]
        else:
            self[updateX][updateY] = [newR,newG,newB,NeighbourCounter, 0]

def CircularNeighbourGenerator(radius):
    '''
    Yield the 4 immediately adjacent pixels
    '''
    def CircularNeighbourGeneratorWithRadius(x,y):
        for newx, newy, dx, dy in ((x+dx,y+dy, dx, dy) 
                                   for dy in range(-radius,radius) 
                                   for dx in range(-radius,radius) 
                                   if (not (dx == 0 and dy == 0) 
                                       and abs(dx)+abs(dy) <= 1.5*radius)):
            yield (newx,newy,abs(dy)+abs(dx) == 1)
    return CircularNeighbourGeneratorWithRadius
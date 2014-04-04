'''
Created on Apr 1, 2014

@author: tdeith
'''
from xmlrpclib import MAXINT
from math import sqrt

class SearchableColourSpace(object):
    '''
    This is a quickly-searchable 3D space representing all unique colour possibilities. 
    This space is optimized for repeated nearest-neighbour searches.
    '''


    def __init__(self, colourBits):
        '''
        Constructor
        '''
        self._searchSpace = [[[-1 for x in xrange(2**colourBits)]  # @UnusedVariable
                                 for x in xrange(2**colourBits)]  # @UnusedVariable
                                 for x in xrange(2**colourBits)]  # @UnusedVariable
        self._width = 2**colourBits
        

    def FindFirstNeighbours(self, R, G, B, ForceExhaustive = False):
        if (ForceExhaustive):
            self._searchAllRGB()
        else:
            while ( self._searchRadius < self._width and len(self._found) == 0 ):
    
                # Set the current search radius, increment the next search radius
                self._searchRadius = self._nextSearchRadius
                self._nextSearchRadius = self._searchRadius + 1
    
                # Set this iteration's max/min RGB values - these correspond to planes which
                #    will be searched later.
                
                self._maxR = min(int(round(R + self._searchRadius)), self._width - 1)
                self._maxG = min(int(round(G + self._searchRadius)), self._width - 1)
                self._maxB = min(int(round(B + self._searchRadius)), self._width - 1)
                self._minR = max(int(round(R - self._searchRadius)), 0)
                self._minG = max(int(round(G - self._searchRadius)), 0)
                self._minB = max(int(round(B - self._searchRadius)), 0)
                
                # Search the max/min RGB planes, unless these planes have already been searched.
            
                if (R + self._searchRadius <= self._width):
                    self._searchMaxR()
                if (R - self._searchRadius >= 0):
                    self._searchMinR()
                if (G + self._searchRadius <= self._width):
                    self._searchMaxG()
                if (G - self._searchRadius >= 0):
                    self._searchMinG()
                if (B + self._searchRadius <= self._width):
                    self._searchMaxB()
                if (B - self._searchRadius >= 0):
                    self._searchMinB()

    def GetNearestNeighbours(self, (R, G, B)):
        
        # Initialize the search radius, and best-found radius
        self._searchRadius = 0
        self._nextSearchRadius = 0
        self._bestFoundItemRadius = MAXINT
        
        # Initialize item lists
        self._found = []
        self._entriesToUpdate = []
        
        # Store the ideal RGB value
        ( self._idealR, self._idealG,  self._idealB ) = (R,G,B)
        
        # Discretize R,G,B for use in Cartesian-y index-y arithmetics 
        R = int(round(R))
        G = int(round(G))
        B = int(round(B))
        
        # DEBUG: print "Target is",R,G,B
        
        self.FindFirstNeighbours(R, G, B)
            
        while (len(self._found) == 0):
            print "AAACH!", R,G,B
            self.FindFirstNeighbours(R, G, B, ForceExhaustive = True)
        
        averageRadiusFromFoundToCenter = sqrt((R - self._found[0][0])**2 + 
                                              (G - self._found[0][1])**2 + 
                                              (B - self._found[0][2])**2)

        self._searchSpace[R][G][B] = averageRadiusFromFoundToCenter

        for (curR, curG, curB) in self._entriesToUpdate:
            curRadius = sqrt((curR - R)**2 + 
                             (curG - G)**2 + 
                             (curB - B)**2)
            
            self._searchSpace[curR][curG][curB] = max(self._searchSpace[curR][curG][curB], 
                                                      averageRadiusFromFoundToCenter - curRadius)
        
        # DEBUG: print "Found:", self._found,"at:", averageRadiusFromFoundToCenter 
        
        return self._found
            
    def FlagColourAsUsed(self, R=0, G=0, B=0, RGB=None):
        '''
        Marks a colour as having been used 
        '''
        if (RGB is not None):
            R,G,B = RGB
        self._searchSpace[R][G][B] = 0

    def _processEntry(self, R, G, B):
        '''
        Do not call me manually
        Processes a single pixel in the search field
        '''
        currentItem = self._searchSpace[R][G][B]
        currentRadius = sqrt((self._idealR - R)**2 + 
                             (self._idealG - G)**2 + 
                             (self._idealB - B)**2)
        
        if (currentItem == -1):
            if ( currentRadius < self._bestFoundItemRadius ):
                self._found = [(R,G,B)]
                self._bestFoundItemRadius = currentRadius
            elif (currentRadius == self._bestFoundItemRadius ):
                self._found.append((R,G,B))
        else:
            self._nextSearchRadius = max(self._nextSearchRadius, currentItem - currentRadius -1 )
            self._entriesToUpdate.append((R,G,B))
            
    def _searchAllRGB(self):
        '''
        Do not call me manually
        Searches the entire searchable space for the nearest neighbour.
        '''
        for R in xrange(self._width):
            for G in xrange(self._width):
                for B in xrange(self._width):
                    self._processEntry(R, G, B)
            
    def _searchMaxR(self):
        '''
        Do not call me manually
        Searches a square along the current MaxR plane
        '''
        R = self._maxR
        for G in range(self._minG, self._maxG+1):
            for B in range(self._minB, self._maxB+1):
                self._processEntry(R, G, B)
                    
    def _searchMinR(self):
        '''
        Do not call me manually
        Searches a square along the current MinR plane
        '''
        R = self._minR
        for G in range(self._minG, self._maxG+1):
            for B in range(self._minB, self._maxB+1):
                self._processEntry(R, G, B)                
                    
    def _searchMaxG(self):
        '''
        Do not call me manually
        Searches a square along the current MaxG plane
        '''
        G = self._maxG
        for B in range(self._minB, self._maxB+1):
            for R in range(self._minR, self._maxR+1):
                self._processEntry(R, G, B)
                
    def _searchMinG(self):
        '''
        Do not call me manually
        Searches a square along the current MinG plane
        '''
        G = self._minG
        for B in range(self._minB, self._maxB+1):
            for R in range(self._minR, self._maxR+1):
                self._processEntry(R, G, B)
                
    def _searchMaxB(self):
        '''
        Do not call me manually
        Searches a square along the current MaxB plane
        '''
        B = self._maxB
        for R in range(self._minR, self._maxR+1):
            for G in range(self._minG, self._maxG+1):
                self._processEntry(R, G, B)

    def _searchMinB(self):
        '''
        Do not call me manually
        Searches a square along the current MinB plane
        '''
        B = self._minB
        for R in range(self._minR, self._maxR+1):
            for G in range(self._minG, self._maxG+1):
                self._processEntry(R, G, B)
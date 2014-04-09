'''
Created on Apr 3, 2014

@author: tdeith
'''

class ColourBucket(object):
    '''
    classdocs
    '''


    def __init__(self, midR, midG, midB, size, limit, parent = None):
        '''
        Constructor
        '''
        
        self.Parent = parent
        self.Size = size
        
        self.MidR = midR
        self.MidG = midG
        self.MidB = midB
        
        # The sum number of colours contained in this bucket
        self.Population = 0

        self.Children = []
        self.HasChildren = False
        
        # The center-to-vertice distance, with sqrt(3) approximated to 1.733.
        self.RadiusTolerance = 1.733*2**(size-1)
        
        if size >= limit:
            midSpan = 2.0**(size-2)
            self.HasChildren = True            
            self._indexedChildren = [ColourBucket(midR+dR,midG+dG,midB+dB, 
                                            size-1, limit, self) 
                               for dB in [-midSpan, midSpan]
                               for dG in [-midSpan, midSpan]
                               for dR in [-midSpan, midSpan]]
            
def AddColour (self, (R, G, B),(x,y)):
    rCoord = R>=self.MidR
    gCoord = G>=self.MidG
    bCoord = B>=self.MidB
    
    if ( self.HasChildren ):
        AddColour(self._indexedChildren[rCoord + 2*gCoord + 4*bCoord], (R,G,B), (x,y))
    else:
        self.Children.append([R,G,B,x,y])
        
    if (self.Population == 0 and self.Parent is not None):
        self.Parent.Children.append(self)
    self.Population += 1

def RemoveColour (self, (R, G, B),(x,y)): 
    rCoord = R>=self.MidR
    gCoord = G>=self.MidG
    bCoord = B>=self.MidB
    
    if ( self.HasChildren ):
        RemoveColour(self._indexedChildren[rCoord + 2*gCoord + 4*bCoord], (R,G,B), (x,y))
    else:
        self.Children.remove([R,G,B,x,y])
        
    self.Population -= 1
    if (self.Population == 0 and self.Parent is None):
        pass
    
    if (self.Population == 0 and self.Parent is not None):
        self.Parent.Children.remove(self)
    
def UpdateColour (self, (oldR,oldG,oldB), (newR,newG,newB), (x,y)):
    oldRCoord = oldR>=self.MidR
    oldGCoord = oldG>=self.MidG
    oldBCoord = oldB>=self.MidB

    newRCoord = newR>=self.MidR
    newGCoord = newG>=self.MidG
    newBCoord = newB>=self.MidB

    if ( self.HasChildren ): 
        if ((oldRCoord, oldGCoord, oldBCoord) == (newRCoord, newGCoord, newBCoord)):
            UpdateColour(self._indexedChildren[oldRCoord+2*oldGCoord+4*oldBCoord], (oldR,oldG,oldB), (newR,newG,newB), (x,y))
        else: 
            RemoveColour(self._indexedChildren[oldRCoord+2*oldGCoord+4*oldBCoord], (oldR,oldG,oldB), (x,y))
            AddColour(self._indexedChildren[newRCoord+2*newGCoord+4*newBCoord], (newR,newG,newB), (x,y))
    else:
        self.Children.remove([oldR,oldG,oldB,x,y])
        self.Children.append([newR,newG,newB,x,y])
        
def GetBucketNearest(self, (R, G, B)):
    rCoord = R>=self.MidR
    gCoord = G>=self.MidG
    bCoord = B>=self.MidB
    if (self.HasChildren):
        return GetBucketNearest(self._indexedChildren[rCoord + 2*gCoord + 4*bCoord],(R,G,B))
    else:
        return self
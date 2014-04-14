'''
Created on Apr 3, 2014

@author: tdeith
'''

sizeLimit = 0

class ColourBucket(object):
    '''
    classdocs
    '''



    def __init__(self, midR, midG, midB, size, limit = -1, parent = None):
        '''
        Constructor
        '''
        global sizeLimit

        if limit != -1:
            sizeLimit = limit
        
        self.Parent = parent
        self.Size = int(size)
        
        
        self.MidR = int(midR)
        self.MidG = int(midG)
        self.MidB = int(midB)
        
        # The sum number of colours contained in this bucket
        self.Population = 0

        self.Children = []
        self.HasChildren = False
        
        # The center-to-vertice distance, with sqrt(3) approximated to 1.733.
        self.RadiusTolerance = int(2**size)
        
        if size > sizeLimit:
            self.HasChildren = True
            self._indexedChildren = [None] * 8
            
def AddColour (node, (R, G, B, x, y, intervalCount)):
    rCoord = R>=node.MidR
    gCoord = G>=node.MidG
    bCoord = B>=node.MidB
    
    if ( node.HasChildren ):
        if (node.Population == 0):
            dR = 1 if rCoord else -1
            dG = 1 if gCoord else -1
            dB = 1 if bCoord else -1
            midDisplace = 2**(node.Size-2)
            newChild = ColourBucket(node.MidR + midDisplace * dR, 
                                    node.MidG + midDisplace * dG,
                                    node.MidB + midDisplace * dB,
                                    node.Size-1, 
                                    parent = node)
            node._indexedChildren [rCoord + 2*gCoord + 4*bCoord] = newChild
            node.Children.append(newChild)  
        AddColour(node._indexedChildren[rCoord + 2*gCoord + 4*bCoord], (R, G, B, x, y, intervalCount))
    else:
        node.Children.append([R,G,B,x,y,intervalCount])
        
    node.Population += 1

def RemoveColour (node, (R, G, B, x, y,intervalCount)): 
    rCoord = R>=node.MidR
    gCoord = G>=node.MidG
    bCoord = B>=node.MidB
    
    if ( node.HasChildren ):
        child = node._indexedChildren[rCoord + 2*gCoord + 4*bCoord]
        RemoveColour(child, (R, G, B, x, y, intervalCount))
        if (child.Population == 0):
            node._indexedChildren[rCoord + 2*gCoord + 4*bCoord] = None
            node.Children.remove(child)
            del(child)
    else:
        node.Children.remove([R,G,B,x,y,intervalCount])
        
    node.Population -= 1
    
def UpdateColour (node, (oldR,oldG,oldB), (newR,newG,newB), (x,y), intervalCount):
    oldRCoord = oldR>=node.MidR
    oldGCoord = oldG>=node.MidG
    oldBCoord = oldB>=node.MidB

    newRCoord = newR>=node.MidR
    newGCoord = newG>=node.MidG
    newBCoord = newB>=node.MidB

    if ( node.HasChildren ): 
        if ((oldRCoord, oldGCoord, oldBCoord) == (newRCoord, newGCoord, newBCoord)):
            UpdateColour(node._indexedChildren[oldRCoord+2*oldGCoord+4*oldBCoord], (oldR,oldG,oldB), (newR,newG,newB), (x,y), intervalCount)
        else: 
            RemoveColour(node._indexedChildren[oldRCoord+2*oldGCoord+4*oldBCoord], (oldR,oldG,oldB, x, y, intervalCount))
            AddColour(node._indexedChildren[newRCoord+2*newGCoord+4*newBCoord], (newR,newG,newB, x, y, intervalCount))
    else:
        node.Children.remove([oldR,oldG,oldB,x,y,intervalCount])
        node.Children.append([newR,newG,newB,x,y,intervalCount])
        
def DeleteNode(node):
    if node.HasChildren:
        for child in node._indexedChildren:
            DeleteNode(child)
    else:
        del (node.Children)
    del (node)
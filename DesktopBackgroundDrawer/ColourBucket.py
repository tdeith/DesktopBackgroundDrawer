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
        self.RadiusTolerance = 2**size
        
        if size >= limit:
            AddChildren(self, midR, midG, midB, size, limit)
            
def AddChildren(Node, midR, midG, midB, size, limit):
    midSpan = 2.0 ** (size - 2)
    Node.HasChildren = True
    Node._indexedChildren = [ColourBucket(midR + dR, 
                                          midG + dG, 
                                          midB + dB, 
                                          size - 1, 
                                          limit, 
                                          Node) 
                                 for dB in [-midSpan, midSpan] 
                                 for dG in [-midSpan, midSpan] 
                                 for dR in [-midSpan, midSpan]]
            
def AddColour (node, (R, G, B, x, y, intervalCount)):
    rCoord = R>=node.MidR
    gCoord = G>=node.MidG
    bCoord = B>=node.MidB
    
    if ( node.HasChildren ):
        AddColour(node._indexedChildren[rCoord + 2*gCoord + 4*bCoord], (R, G, B, x, y, intervalCount))
    else:
        node.Children.append([R,G,B,x,y,intervalCount])
        
    if (node.Population == 0 and node.Parent is not None):
        node.Parent.Children.append(node)
    node.Population += 1

def RemoveColour (node, (R, G, B, x, y,intervalCount)): 
    rCoord = R>=node.MidR
    gCoord = G>=node.MidG
    bCoord = B>=node.MidB
    
    if ( node.HasChildren ):
        RemoveColour(node._indexedChildren[rCoord + 2*gCoord + 4*bCoord], (R, G, B, x, y, intervalCount))
    else:
        node.Children.remove([R,G,B,x,y,intervalCount])
        
    node.Population -= 1
    if (node.Population == 0 and node.Parent is None):
        pass
    
    if (node.Population == 0 and node.Parent is not None):
        node.Parent.Children.remove(node)
    
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
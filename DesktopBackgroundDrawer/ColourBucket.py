'''
Created on Apr 3, 2014

@author: tdeith
'''

class ColourBucket(object):
    '''
    classdocs
    '''

    def __init__(self, midR, midG, midB, size, limit):
        '''
        Constructor
        '''
        
        self.MidR = midR
        self.MidG = midG
        self.MidB = midB
        
        # The sum number of colours contained in this bucket
        self.Population = 0

        self.Children = []
        self.HasChildren = False
        
        # The (very very approximate) center-to-vertice distance, with sqrt(3) approximated to 2
        self.Size = size
        
        CreateNextChildren(self, midR, midG, midB, size, limit)

def CreateNextChildren(node, midR, midG, midB, size, limit):
    if size >= limit:
        midSpan = 2.0 ** (size - 2)
        node.HasChildren = True
        try:
            node._indexedChildren = [ColourBucket(midR + dR, midG + dG, midB + dB, 
                    size - 1, limit) for 
                dB in [-midSpan, midSpan] for 
                dG in [-midSpan, midSpan] for 
                dR in [-midSpan, midSpan]]
        except MemoryError:
            print "Child ", node.Size
            print "Centered at ", node.MidB, node.MidG, node.MidR
            raise MemoryError
            
def AddColour (node, (R, G, B,x,y,intervalAdded)):
    rCoord = R>=node.MidR
    gCoord = G>=node.MidG
    bCoord = B>=node.MidB
    
    if ( node.HasChildren ):
        AddColour(node._indexedChildren[rCoord + 2*gCoord + 4*bCoord], (R,G,B,x,y,intervalAdded))
    else:
        node.Children.append([R,G,B,x,y,intervalAdded])
        
    if (node.Population == 0 and node.Parent is not None):
        node.Parent.Children.append(node)
    node.Population += 1

def RemoveColour (node, (R, G, B,x,y,intervalAdded)): 
    rCoord = R>=node.MidR
    gCoord = G>=node.MidG
    bCoord = B>=node.MidB
    
    if ( node.HasChildren ):
        RemoveColour(node._indexedChildren[rCoord + 2*gCoord + 4*bCoord], (R,G,B,x,y,intervalAdded))
    else:
        node.Children.remove([R,G,B,x,y,intervalAdded])
        
    node.Population -= 1
    if (node.Population == 0 and node.Parent is None):
        pass
    
    if (node.Population == 0 and node.Parent is not None):
        node.Parent.Children.remove(node)
    
def UpdateColour (node, (oldR,oldG,oldB, newR,newG,newB, x,y, intervalAdded)):
    oldRCoord = oldR>=node.MidR
    oldGCoord = oldG>=node.MidG
    oldBCoord = oldB>=node.MidB

    newRCoord = newR>=node.MidR
    newGCoord = newG>=node.MidG
    newBCoord = newB>=node.MidB

    if ( node.HasChildren ): 
        if ((oldRCoord, oldGCoord, oldBCoord) == (newRCoord, newGCoord, newBCoord)):
            UpdateColour(node._indexedChildren[oldRCoord+2*oldGCoord+4*oldBCoord], (oldR,oldG,oldB,newR,newG,newB,x,y,intervalAdded))
        else: 
            RemoveColour(node._indexedChildren[oldRCoord+2*oldGCoord+4*oldBCoord], (oldR,oldG,oldB,x,y,intervalAdded))
            AddColour(node._indexedChildren[newRCoord+2*newGCoord+4*newBCoord], (newR,newG,newB,x,y,intervalAdded))
    else:
        node.Children.remove([oldR,oldG,oldB,x,y,intervalAdded])
        node.Children.append([newR,newG,newB,x,y,intervalAdded])
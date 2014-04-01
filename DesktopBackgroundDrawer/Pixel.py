'''
Created on Mar 7, 2014

@author: tdeith
'''

class Pixel(object):
    '''
    The pixel class is used to represent a single pixel, with accessors to the neighbours of that pixel, 
    the pixel's colour, and pixel's location.  
    '''

    def __init__(self):
        self.CompletedNeighbours = 0
        self.ContainedColour = (0,0,0)
        
    def UpdateTarget(self, nextColour):
        if (self.CompletedNeighbours == -1):
            return

        elif ( self.CompletedNeighbours == 0 ):
            self.TargetColour = nextColour
        else:  
            self.TargetColour[0] = float(self.TargetColour[0] * self.CompletedNeighbours + nextColour[0])/(self.CompletedNeighbours + 1)
            self.TargetColour[1] = float(self.TargetColour[1] * self.CompletedNeighbours + nextColour[1])/(self.CompletedNeighbours + 1)
            self.TargetColour[2] = float(self.TargetColour[2] * self.CompletedNeighbours + nextColour[2])/(self.CompletedNeighbours + 1)
    
        self.CompletedNeighbours += 1
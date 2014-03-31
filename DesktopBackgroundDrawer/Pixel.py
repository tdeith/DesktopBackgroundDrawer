'''
Created on Mar 7, 2014

@author: tdeith
'''

from Colour import Colour

class Pixel(object):
    '''
    The pixel class is used to represent a single pixel, with accessors to the neighbours of that pixel, 
    the pixel's colour, and pixel's location.  
    '''

    def __init__(self, x = 0, y = 0, colour = Colour(), targetColour=Colour()):
        self.X, self.Y = x,y
        self.Colour = colour
        self.TargetColour = targetColour
        self.QueueIndex = -1
        self.CompletedNeighbours = 0
        
    def UpdateTarget(self, nextColour): 
        self.TargetColour.R = float(self.TargetColour.R * self.CompletedNeighbours + nextColour.R)/(self.CompletedNeighbours + 1)
        self.TargetColour.G = float(self.TargetColour.G * self.CompletedNeighbours + nextColour.G)/(self.CompletedNeighbours + 1)
        self.TargetColour.B = float(self.TargetColour.B * self.CompletedNeighbours + nextColour.B)/(self.CompletedNeighbours + 1)
    
        self.CompletedNeighbours += 1
        
    def printColour(self):
        print self.Colour.R, self.Colour.G, self.Colour.B
        
    def printTarget(self):
        print self.TargetColour.R, self.TargetColour.G, self.TargetColour.B
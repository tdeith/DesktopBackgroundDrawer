'''
Created on Mar 7, 2014

@author: tdeith
'''

class Colour():
    '''
    A class for storing a colour, and retrieving/comparing that colour's RGB/HSL values.  
    '''
    
    # Initalize a new colour. Can include RGB tuple as parameter.
    def __init__(self, R = 0, G = 0, B = 0, RGB = None):
        if (RGB is not None): 
            self.R, self.G, self.B = RGB
        else:    
            self.R, self.G, self.B =  R, G, B
    
    
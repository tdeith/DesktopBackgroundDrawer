'''
Created on Apr 3, 2014

@author: tdeith
'''

class PixelList(object):
    '''
    This class represents a collection of pixels, along with useful methods for storing or 
    fetching these pixels.
    '''


    def __init__(self, width, height, dataDimensions = 3):
        '''
        Constructor
        '''
        
        # Make sure this is large enough to contain RGB values, the bare minimum of a pixel.
        if (dataDimensions < 3):
            raise ValueError("The number of data dimensions supplied to the \
PixelList is too small to hold R,G,B values.")
        
        # Create the width*height pixel array
        self._pixels = [[[0 for n in xrange(dataDimensions)]      # @UnusedVariable
                            for y in xrange(height)]             # @UnusedVariable
                            for x in xrange(width)]               # @UnusedVariable

        self.Width = width
        self.Height = height
        
    def __getitem__(self, index):
        '''
        Let's allow interfacing as though this is actually a list...
        '''
        return self._pixels[index]        

    
    def FlatRows(self):
        '''
        Generate rows of pixels, formatted to be flat (1-D) lists 
        (i.e, [0,0,0, 0,0,0, 0,0,0] instead of 
              [(0,0,0),(0,0,0),(0,0,0)] )
        '''
        for row in list(zip(*self)):
            RGBRow = []
            for pixel in row:
                RGBRow.extend((int(pixel[0]), int(pixel[1]), int(pixel[2])))
            yield RGBRow
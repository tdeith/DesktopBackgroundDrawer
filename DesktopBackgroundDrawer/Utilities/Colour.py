'''
Created on Mar 7, 2014

@author: tdeith
'''

class Colour():
    '''
    A class for storing a colour, and retrieving that colour's RGB/HSL values.  
    '''
    
    # Initalize a new colour. Can include RGB tuple as parameter.
    def __init__(self, R = 0, G = 0, B = 0):
        # See if the colours are actually cast-able as ints
        try:
            R,G,B = int(R), int(G), int(B)
        except (TypeError, AttributeError) as exception:
            print "Error on Colour initialization! RGB arguments ( {0}, {1}, {2} ) contains a variable not able to be cast as an int!".format(R,G,B)
            raise exception
        
        # Test that the colour values are in range
        if ( max(R, G, B) > 255 or min( R , G , B ) < 0):
            R,G,B = max(min(R,0),255), max(min(G,0),255), max(min(B,0),255)
            print "Error on Colour initialization! Initialized RGB value of ( {0}, {1}, {2} ) is out of bounds".format(R,G,B)
            raise ValueError()
 
        (self.R, self.G, self.B) =  R , G , B
    
    # Retrieves the Hue for this colour instance. This algorithm is pretty funny... 
    def GetHue(self):
        cmax = max(self.R, self.G, self.B)
        cmin = min(self.R, self.G, self.B)
        if ( self.R == cmax):
            return (60* ( (self.G-self.B)/(cmax-cmin)%6))
        elif (self.G == cmax):
            return (60* ( (self.B-self.R)/(cmax-cmin)+2))
        elif (self.B == cmax):
            return (60* ( (self.R-self.G)/(cmax-cmin)+4))
        
    # Retrieves the Saturation for this colour instance
    def GetSat(self):
        cmax = max(self.R, self.G, self.B)
        cmin = min(self.R, self.G, self.B)
        if (cmax == cmin):
            # Avoid dividing by zero 
            return 0
        else:
            return ( (cmax - cmin) / (1-abs(cmax + cmin - 1 ) ) )
            
    # Retrieves the Light Level for this colour instance
    def GetLight(self):
        cmax = max(self.R, self.G, self.B)
        cmin = min(self.R, self.G, self.B)
        return (cmax + cmin)/2
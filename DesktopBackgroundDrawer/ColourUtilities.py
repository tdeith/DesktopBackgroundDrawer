'''
Created on Apr 1, 2014

@author: tdeith
'''

# Retrieves the Hue for this colour. This algorithm is pretty funny... 
def GetHue(colour):
    cmax = max(colour[0], colour[1], colour[2])
    cmin = min(colour[0], colour[1], colour[2])
    if ( colour[0] == colour[1] == colour[2]) : return 0
    if ( colour[0] == cmax):
        return (60* ( float(colour[1]-colour[2])/(cmax-cmin)%6))
    elif (colour[1] == cmax):
        return (60* ( float(colour[2]-colour[0])/(cmax-cmin)+2))
    elif (colour[2] == cmax):
        return (60* ( float(colour[0]-colour[1])/(cmax-cmin)+4))
    
# Retrieves the Saturation for this colour
def GetSat(colour):
    cmax = max(colour[0], colour[1], colour[2])
    cmin = min(colour[0], colour[1], colour[2])
    if (abs(cmax + cmin - 1 ) == 1):
        # Avoid dividing by zero 
        return 0
    else:
        return ( (cmax - cmin) / (1-abs(cmax + cmin - 1 ) ) )
        
# Retrieves the Light Level for this colour instance
def GetLight(colour):
    cmax = max(colour[0], colour[1], colour[2])
    cmin = min(colour[0], colour[1], colour[2])
    return (cmax + cmin)/2

# Get's the angular distance between two hues
def GetHueDist(colour1, colour2):
    diff = abs(GetHue(colour1) - GetHue(colour2))

    if (diff > 180):
        diff = abs(diff - 360)
          
    return diff
    

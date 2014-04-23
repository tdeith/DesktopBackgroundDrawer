import random
from collections import deque
from ColourUtilities import GetHue, GetHueDist, GetSat, IsInHueRange

def RandomColourList(colourBits, colourReuse):
    print "\nMaking the shuffled list of colours. This is RAM heavy."
    allColours = [(R,G,B)
                    for B in xrange(2**colourBits) 
                    for G in xrange(2**colourBits)
                    for R in xrange(2**colourBits)] * colourReuse
    
    random.shuffle(allColours)
    print "    Done."    
    return deque(allColours)

def SortedHueColourList(colourBits, colourReuse):
    startingHue = random.randint(0,360)
    maxQueueSize = 2**20    
    hueIterations = max(1, int((colourReuse * 2**(3*colourBits))/maxQueueSize))
    hueWalkDistance = 360.0 / hueIterations
    minHue = startingHue
    maxHue = ( startingHue + hueWalkDistance ) % 360.0
    for i in xrange(hueIterations):
        print "\nMaking the list of which colours will be used next. (List iteration " + str(i+1) + ")..."
        isInRange = IsInHueRange(minHue, maxHue)
        colourSelection = deque(sorted([(R,G,B) 
                                  for B in xrange(2**colourBits) 
                                  for G in xrange(2**colourBits)
                                  for R in xrange(2**colourBits)
                                  if (isInRange(GetHue((R,G,B))))]* colourReuse,
                           lambda RGB1,RGB2 : cmp(GetHue(RGB1), GetHue(RGB2))))
        if hueIterations == 1:
            colourSelection.rotate(int((len(colourSelection)-1)*startingHue/360.0))
        print "    Done. Got " + str(len(colourSelection)) + " colours."
        for colour in colourSelection: 
            yield colour
        minHue = maxHue
        maxHue = ( maxHue + hueWalkDistance ) % 360.0

def SortedDivergingHueColourList(colourBits, colourReuse):
    startingHue = random.randint(0,360)
    maxQueueSize = 2**20
    hueIterations = max(1, int((colourReuse * 2**(3*colourBits))/maxQueueSize))
    hueWalkDistance = 180.0 / hueIterations
    minHueDiff = 0
    maxHueDiff = ( startingHue + hueWalkDistance ) % 180.0
    for i in xrange(hueIterations):
        print "\nMaking the list of which colours will be used next. (List iteration " + str(i+1) + ")..."
        colourSelection = sorted([(R,G,B) 
                                for B in xrange(2**colourBits) 
                                for G in xrange(2**colourBits)
                                for R in xrange(2**colourBits)
                                if ((GetHueDist((R,G,B), None, startingHue) < maxHueDiff) and
                                    (GetHueDist((R,G,B), None, startingHue) >= minHueDiff))] * colourReuse,
                            lambda RGB1,RGB2 : cmp(abs(startingHue - GetHue(RGB1)), 
                                                   abs(startingHue - GetHue(RGB2))))
        print "    Done. Got " + str(len(colourSelection)) + " colours."
        for colour in colourSelection:
            yield colour
        minHueDiff = maxHueDiff
        maxHueDiff = ( maxHueDiff + hueWalkDistance ) % 180.0
        
def SteppedSatSortedHueColourList(colourBits, colourReuse, stepBrackets = [0.3]):
    stepBrackets = sorted(stepBrackets, None, None, True)
    if (0 not in stepBrackets): stepBrackets.append(0)
    
    maxQueueSize = 2**15
    currentMaxSat = 1 
    startingHue = random.randint(0,360)
    i = 0
    
    for j, currentMinSat in enumerate(stepBrackets):
        print "\nGenerating colour lists using the next bracket of saturations (bracket iteration " + str(j+1) + ")."
        hueIterations = max(1, int(((currentMaxSat - currentMinSat ) * 
                                    colourReuse * 
                                    2**(3*colourBits)) / 
                                   maxQueueSize))
        hueWalkDistance = 360.0 / hueIterations
        minHue = startingHue
        maxHue = ( startingHue + hueWalkDistance ) % 360.0
        
        for k in xrange(hueIterations):  # @UnusedVariable
            print "\nMaking the list of which colours will be used next. (List iteration " + str(i+1) + ")..."
            i += 1
            isInRange = IsInHueRange(minHue, maxHue)
            colourSelection = deque(sorted([(R,G,B) 
                                      for B in xrange(2**colourBits) 
                                      for G in xrange(2**colourBits)
                                      for R in xrange(2**colourBits)
                                      if (isInRange(GetHue((R,G,B))) 
                                          and currentMinSat <= GetSat((R,G,B), colourBits) 
                                          and currentMaxSat >= GetSat((R,G,B), colourBits))]
                                           * colourReuse,
                               lambda RGB1,RGB2 : cmp(GetHue(RGB1), GetHue(RGB2))))
            if hueIterations == 1:
                colourSelection.rotate(int((len(colourSelection)-1)*startingHue/360.0))
            print "    Done. Got " + str(len(colourSelection)) + " colours."
            for colour in colourSelection: 
                yield colour
            minHue = maxHue
            maxHue = ( maxHue + hueWalkDistance ) % 360.0
        
        currentMaxSat = currentMinSat
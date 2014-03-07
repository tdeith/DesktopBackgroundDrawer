'''
Created on Mar 7, 2014

@author: tdeith
'''

from Queue import *

class PanelQueue(Queue):
    '''
    A list of panels neighbours have not yet been determined
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        super(PanelQueue, self).__init__(params)       
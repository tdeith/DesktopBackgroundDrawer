'''
Created on Mar 7, 2014

@author: tdeith
'''

from Queue import Queue

class PixellQueue(Queue):
    '''
    A list of pixels whose neighbours have not yet been determined
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        super(PixellQueue, self).__init__(params)
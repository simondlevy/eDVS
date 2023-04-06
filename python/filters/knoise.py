'''
DVS event filtersing

Adapted from Java code in
  https:#github.com/SensorsINI/jaer/tree/master/src/net/sf/jaer/eventprocessing/filter

Copyright (C) 2023 Simon D. Levy

MIT License
'''

import numpy as np


class ONFilter:

    DEFAULT_TIMESTAMP = 0

    def __init__(self):

        pass


    def check(self, e):
        '''
        Returns True if event e passes filter, False otherwise
        '''

        return True

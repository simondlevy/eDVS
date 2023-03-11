'''
eDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import serial
import time

class eDVS:

    QSIZE = 1000

    def __init__(self, port):
        '''
        Creates an eDVS object.
        params:
            port - port ID ('COM5', '/dev/ttyUSB0', etc.)
        '''

        # Circular event queue
        self.queue = [None] * self.QSIZE
        self.qpos = 0

        self.port = port

        self.done = False

    def start(self):
        '''
        Initiates communication with the eDVS.
        '''


        # Every other byte represents a completed event
        x    = None
        gotx = False

        # Flag will be set on main thread when user quits
        while not self.done:

            # Read a byte from the sensor
            b = ord(self.port.read())

            # Value is in rightmost seven bits
            v = b & 0b01111111

            # Isolate first bit
            f = b>>7

            # Correct for misaligned bytes
            if f==0 and not gotx:
                gotx = not gotx

            # Second byte; record event
            if gotx:
                y = v
                p = 2*f-1 # Convert event polarity from 0,1 to -1,+1
                self.queue[self.qpos] = (x,y,p)
                self._advance()

            # First byte; store X
            else:
                x = v

            gotx = not gotx


    def hasNext(self):

        return self.queue[self.qpos] is not None

    def next(self):

        e = self.queue[self.qpos]
        self.queue[self.qpos] = None
        self._advance()
        return e

    def _advance(self):
        
        self.qpos = (self.qpos+1) % self.QSIZE

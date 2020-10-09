#!/usr/bin/env python3
'''
eDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import serial
import time

class eDVS:

    QSIZE = 1000

    def __init__(self, port, baudrate=12000000):
        '''
        Creates an eDVS object.
        params:
            port - port ID ('COM5', '/dev/ttyUSB0', etc.)
        '''

        # Circular event queue
        self.queue = [None] * self.QSIZE
        self.qpos = 0

        self.port = serial.Serial(port=port, baudrate=baudrate)

        self.done = False

    def start(self):
        '''
        Initiates communication with the eDVS.
        '''

        # Reset board
        self._send('R')

        # Enable event sending
        self._send('E+')

        # Use two-byte event format
        self._send('!E0')

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
                t = time.time()
                y = v
                p = 2*f-1 # Convert event polarity from 0,1 to -1,+1
                self.queue[self.qpos] = (x,y,p,t)
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

    def stop(self):
        '''
        Terminates communication with the eDVS.
        '''

        self.done = True
        self._send('E-')
        self.port.close()

    def _send(self, cmd):

        self.port.write((cmd + '\n').encode())
        time.sleep(.01)
                

    def _advance(self):
        
        self.qpos = (self.qpos+1) % self.QSIZE

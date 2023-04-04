'''
EDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import serial
import time


class EDVS:

    QSIZE = 1000

    def __init__(self, port,
                 baudrate=12000000, use_filter=False, use_timestamp=False):
        '''
        Creates an EDVS object.
        params:
            port - port ID ('COM5', '/dev/ttyUSB0', etc.)
        '''

        self.port = serial.Serial(port=port, baudrate=baudrate)

        # Circular event queue
        self.queue = [None] * self.QSIZE
        self.qpos = 0

        self.done = False

        self.use_filter = use_filter
        self.use_timestamp = use_timestamp

    def start(self):
        '''
        Initiates communication with the EDVS.
        '''

        # Reset board
        self._send('R')

        # Enable event sending
        self._send('E+')

        # Specify event format (no timestamp or 32-bit timestamp)
        self._send('!E' + ('6' if self.use_timestamp else '0'))

        # Every other byte represents a completed event
        x = None
        gotx = False

        # Flag will be set on main thread when user quits
        while not self.done:

            # Read a byte from the sensor
            b = ord(self.port.read())

            # Value is in rightmost seven bits
            v = b & 0b01111111

            # Isolate first bit
            f = b >> 7

            # Correct for misaligned bytes
            if f == 0 and not gotx:
                gotx = not gotx

            # Second byte; record event
            if gotx:
                y = v
                p = 2*f-1  # Convert event polarity from 0,1 to -1,+1
                self.queue[self.qpos] = (x, y, p)
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
        Terminates communication with the EDVS.
        '''

        self.done = True

        self._send('E-')
        self.port.close()

    def version(self):

        self._send('?V')
        self.port.read(4)
        result = ''
        while True:
            c = self.port.read().decode('utf-8')
            if c == '\n':
                break
            result += c
        return result

    def ledOn(self):

        self._led('+')

    def ledOff(self):

        self._led('-')

    def ledBlink(self):

        self._led('.')

    def ledAlarm(self, msec):

        self._led('a=%d' % msec)

    def _led(self, cmd):

        self._send('!L' + cmd)

    def _send(self, cmd):

        self.port.write((cmd + '\n').encode())
        time.sleep(.01)

    def _advance(self):

        self.qpos = (self.qpos+1) % self.QSIZE

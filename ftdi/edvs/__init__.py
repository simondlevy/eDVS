'''
EDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import serial
from time import time, sleep

class Event:

    def __init__(self, x, y, p, t=0):

        self.x = x
        self.y = y
        self.polarity = p
        self.timestamp = t

class EDVS:

    QSIZE = 1000

    def __init__(self, port, baudrate=12000000, event_format=0):
        '''
        Creates an EDVS object.
        params:
            port - port ID ('COM5', '/dev/ttyUSB0', etc.)
        '''

        self.port = serial.Serial(port=port, baudrate=baudrate)

        self.event_format = event_format

        # Circular event queue
        self.queue = [None] * self.QSIZE
        self.qpos = 0

        self.done = False

    def reset(self):

        self._send('R')

    def start(self):
        '''
        Initiates communication with the EDVS.
        '''

        # Reset board
        self.reset()

        # Enable event sending
        self._send('E+')

        # Specify event format 
        self._send('!E%d' % (self.event_format))

        # We need an initial Y coordinate to kick things off
        y = 0

        # We run a finite-state machine to parse the incoming bytes
        state = 0

        # Track system time for event format 0
        time_start = time()

        # Flag will be set on main thread when user quits
        while not self.done:

            # Read a byte from the sensor
            b = ord(self.port.read())

            # Isolate first bit
            b0 = b >> 7

            # Correct for misaligned bytes
            if b0 == 0 and state == 0:
                state = 1

            # First byte; store Y
            if state == 0:
                y = self._byte2coord(b)
                state = 1

            # Second byte; record event
            elif state == 1:

                x = self._byte2coord(b)

                t = int((time() - time_start) * 1e6)

                if self.event_format == 0:
                    self._enqueue(b0, x, y, t)
                    state = 0
                else:
                    state = 2


            else:
                t = (t << 8) | b
                state = (state + 1) % (self.event_format + 2)
                if state == 0:
                    self._enqueue(b0, x, y, t)


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
        sleep(.01)

    def _advance(self):

        self.qpos = (self.qpos+1) % self.QSIZE

    def _byte2coord(self, b):

        return b & 0b01111111

    def _enqueue(self, b0, x, y, t):
        self.queue[self.qpos] = Event(x, y, bool(b0), t)
        self._advance()



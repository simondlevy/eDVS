'''
EDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import serial
import time


class EDVS:

    QSIZE = 1000

    def __init__(self, port, baudrate=12000000):
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

    def byte2event(self, b):

        return b & 0b01111111, 2 * (b >> 7) - 1

    def start(self):
        '''
        Initiates communication with the EDVS.
        '''

        # Reset board
        self._send('R')

        # Enable event sending
        self._send('E+')

        # Specify event format (no timestamp or 32-bit timestamp)
        # self._send('!E6')
        self._send('!E0')

        # Every other byte represents a completed event
        x = None
        state = 0

        # Flag will be set on main thread when user quits
        while not self.done:

            # Read a byte from the sensor
            b = ord(self.port.read())

            if state == 0:
                x, _ = self.byte2event(b)
                state = 1

            # Second byte; record event
            elif state == 1:
                y, p = self.byte2event(b)
                self.queue[self.qpos] = (x, y, p)
                self._advance()
                state = 0

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

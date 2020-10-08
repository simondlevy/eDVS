/*
eDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#pragma once

#include <stdint.h>

class eDVS {

    private:

        int8_t   events[128][128];
        uint16_t times[128][128];
        bool done;

    public:

        eDVS(void);

    /*
        # We'll use clock time (instead of event time) for speed
        self.times = np.zeros((128,128))

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
                y = v
                self.events[x,y] = 2*f-1 # Convert event polarity from 0,1 to -1,+1
                self.times[x,y] = time.time()

            # First byte; store X
            else:
                x = v

            gotx = not gotx

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
*/
};

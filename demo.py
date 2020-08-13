#!/usr/bin/env python3
'''
Simple demo of the IniVation eDVS using OpenCV

Copyright (C) 2020 Simon D. Levy

MIT License
'''

# Change this to match your com port (e.g., 'COM5')
PORT = '/dev/ttyUSB0'

# Events older than this time in gotxs get zeroed-out
INTERVAL = 0.10

# Frame rate for saving movie
VIDEO_FPS = 100

# Scale-up factor for display
SCALEUP = 4

import serial
from time import time, sleep
import cv2
import numpy as np
from threading import Thread

class eDVS:

    def __init__(self, port):

        self.port = serial.Serial(port=port, baudrate=12000000, rtscts=True)

        # +/- polarity
        self.events = np.zeros((128,128)).astype('int8')

        # We'll use clock time (instead of event time) for speed
        self.times = np.zeros((128,128))

        self.done = False

    def start(self):

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
                self.times[x,y] = time()

            # First byte; store X
            else:
                x = v

            gotx = not gotx

    def stop(self):

        self.done = True

    def _send(self, cmd):

        self.port.write((cmd + '\n').encode())
        sleep(.01)

def main():

    edvs = eDVS(PORT)

    # Start sensor on its own thread
    thread = Thread(target=edvs.start)
    thread.daemon = True
    thread.start()

    # Create a video file to save the movie
    out = cv2.VideoWriter('movie.avi', cv2.VideoWriter_fourcc('M','J','P','G'), VIDEO_FPS, (128*SCALEUP,128*SCALEUP))

    while(True):

        # Zero out pixels with events older than a certain time before now
        edvs.events[(time() - edvs.times) > INTERVAL] = 0

        # Convert events to large color image
        image = np.zeros((128,128,3)).astype('uint8')
        image[edvs.events==+1,2] = 255
        image[edvs.events==-1,1] = 255
        image = cv2.resize(image, (128*SCALEUP,128*SCALEUP))

        # Write the color image to the video file
        out.write(image)

        # Display the large color image
        cv2.imshow('Mini eDVS', image)

        # Quit on ESCape
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

    edvs.stop()

    thread.join()

if __name__ == '__main__':

    main()

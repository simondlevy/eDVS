#!/usr/bin/env python3
'''
Simple test of the Mini eDVS using OpenCV

Copyright (C) 2020 Simon D. Levy

MIT License
'''

PORT = '/dev/ttyUSB0'

# Events older than this time in seconds get zeroed-out
INTERVAL = 0.10

import serial
from time import time, sleep
import cv2
import numpy as np
from threading import Thread

def send(port, cmd):

    port.write((cmd + '\n').encode())
    sleep(.01)

def read_sensor(events, times, flags):

    port = serial.Serial(port=PORT, baudrate=12000000, rtscts=True)

    # Reset board
    send(port, 'R')

    # Enable event sending
    send(port, 'E+')

    # Use two-byte event format
    send(port, '!E0')

    # Every second byte represents a completed event
    x      = None
    second = False

    while flags[0]:

        # Read a byte from the sensor
        b = ord(port.read())

        # Value is in rightmost seven bits
        v = b & 0b01111111

        # Second byte; record event
        if second:
            y = v
            events[x,y] = 2 * (b>>7) - 1 # Convert event polarity from 0,1 to -1,+1
            times[x,y] = time()

        # First byte; store X
        else:
            x = v

        second = not second

    print('done')

def main():

    events = np.zeros((128,128)).astype('int8')

    times = np.zeros((128,128))

    flags = [True]

    thread = Thread(target=read_sensor, args = (events,times,flags))
    thread.daemon = True
    thread.start()

    while(True):

        # Zero out pixels with events older than a certain time before now
        events[(time() - times) > INTERVAL] = 0

        # Convert events to color image
        image = np.zeros((128,128,3))
        image[events==+1,2] = 1.0
        image[events==-1,1] = 1.0

        # Display the color image at twice original size
        cv2.imshow('image', cv2.resize(image, ((512,512))))
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

    flags[0] = False

    thread.join()

if __name__ == '__main__':

    main()

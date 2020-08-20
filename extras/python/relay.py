#!/usr/bin/env python3
'''
Simple demo of the IniVation eDVS using OpenCV

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from edvs import eDVS
from threading import Thread
from time import time
import cv2
import numpy as np
import argparse
import serial

def grab(flags, portname, baudrate, events, times):

    port = serial.Serial(portname, baudrate)

    x    = None
    gotx = False

    while flags[0]:

        v = ord(port.read(1))

        f = 1

        # Second byte; record event
        if gotx:
            y = v
            events[x,y] = 2*f-1 # Convert event polarity from 0,1 to -1,+1
            times[x,y] = time()

        # First byte; store X
        else:
            x = v

        gotx = not gotx


    port.close()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", required=True, help="Port (/dev/ttyUSB0, COM5, etc.")
    parser.add_argument("-b", "--baud", default=12000000, type=int, help="Baud rate")
    parser.add_argument("-i", "--interval", default=0.10, type=float, help="Fade-out interval for events")
    parser.add_argument("-f", "--fps", default=100, type=int, help="Dispaly frames per second")
    parser.add_argument("-s", "--scaleup", default=4, type=int, help="Scale-up factor")
    parser.add_argument("-m", "--movie", default=None, help="Movie file name")
    args = parser.parse_args()

    events = np.zeros((128,128)).astype('int8')
    times = np.zeros((128,128))

    # Start sensor on its own thread
    #thread = Thread(target=edvs.start)
    flags = [True]
    thread = Thread(target=grab, args=(flags,args.port,args.baud,events,times))
    thread.daemon = True
    thread.start()

    # Create a video file to save the movie if indicated
    out = cv2.VideoWriter(args.movie, cv2.VideoWriter_fourcc('M','J','P','G'), args.fps, (128*args.scaleup,128*args.scaleup)) \
            if args.movie is not None  else None

    while(True):

        # Zero out pixels with events older than a certain time before now
        events[(time() - times) > args.interval] = 0

        # Convert events to large color image
        image = np.zeros((128,128,3)).astype('uint8')
        image[events==+1,2] = 255
        image[events==-1,1] = 255
        image = cv2.resize(image, (128*args.scaleup,128*args.scaleup))

        # Write the movie to the video file if indicated
        if out is not None:
            out.write(image)

        # Display the large color image
        cv2.imshow('Mini eDVS', image)

        # Quit on ESCape
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

    #edvs.stop()

    flags[0] = False

    thread.join()

if __name__ == '__main__':

    main()

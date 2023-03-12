#!/usr/bin/env python3
'''
Gets raw bytes from the Teensy 4.0 board, converts them into events, and
displays them using OpenCV

Copyright (C) 2023 Simon D. Levy

MIT License
'''

import edvs
from threading import Thread
import cv2
import numpy as np
import argparse
import serial

def main():

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-p", "--port", default='/dev/ttyACM0' , help="Port (/dev/ttyUSB0, COM5, etc.")
    argparser.add_argument("-b", "--baud", default=2000000, type=int, help="Baud rate")
    argparser.add_argument("-i", "--interval", default=0.02, type=float, help="Fade-out interval for events")
    argparser.add_argument("-f", "--fps", default=100, type=int, help="Dispaly frames per second")
    argparser.add_argument("-s", "--scaleup", default=4, type=int, help="Scale-up factor")
    argparser.add_argument("-m", "--movie", default=None, help="Movie file name")
    args = argparser.parse_args()

    # Connect to Teensy
    port = serial.Serial(args.port, args.baud)

    # Construct and EDVS parser
    dvsparser = edvs.Parser(port)

    # Start sensor on its own thread
    thread = Thread(target=dvsparser.start)
    thread.daemon = True
    thread.start()

    # Create a video file to save the movie if indicated
    out = cv2.VideoWriter(args.movie, cv2.VideoWriter_fourcc('M','J','P','G'), args.fps, (128*args.scaleup,128*args.scaleup)) \
            if args.movie is not None  else None

    # Track time so we can stop displaying old events
    counts = np.zeros((128,128)).astype('uint8')

    # Start with an empty image
    image = np.zeros((128,128,3)).astype('uint8')

    # Compute number of iterations before events should disappear, based on
    # 1msec display assumption
    ageout = int(args.interval * 1000)

    while(True):

        # Get events from DVS
        while dvsparser.hasNext():
            x,y, p = dvsparser.next()
            image[x,y] = (0,255,0) if p == -1 else (0,0,255)
            counts[x,y] = 1

        # Zero out events older than a certain time before now
        image[counts==ageout] = 0
        counts[counts==ageout] = 0

        # Increase age for events
        counts[counts>0] += 1

        # Scale up the image for visibility
        bigimage = cv2.resize(image, (128*args.scaleup,128*args.scaleup))

        # Write the movie to the video file if indicated
        if out is not None:
            out.write(bigimage)

        # Display the large color image
        cv2.imshow('Mini eDVS', bigimage)

        # Quit on ESCape
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

    dvsparser.stop()

    thread.join()

if __name__ == '__main__':

    main()

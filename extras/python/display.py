#!/usr/bin/env python3
'''
Simple demo of the iniVation eDVS using OpenCV

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from edvs import eDVS
from threading import Thread
from time import time
import cv2
import numpy as np
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", required=True, help="Port (/dev/ttyUSB0, COM5, etc.")
    parser.add_argument("-b", "--baud", default=12000000, type=int, help="Baud rate")
    parser.add_argument("-i", "--interval", default=0.10, type=float, help="Fade-out interval for events")
    parser.add_argument("-f", "--fps", default=100, type=int, help="Dispaly frames per second")
    parser.add_argument("-s", "--scaleup", default=4, type=int, help="Scale-up factor")
    parser.add_argument("-m", "--movie", default=None, help="Movie file name")
    args = parser.parse_args()

    edvs = eDVS(args.port, args.baud)

    # Start sensor on its own thread
    thread = Thread(target=edvs.start)
    thread.daemon = True
    thread.start()

    # Create a video file to save the movie if indicated
    out = cv2.VideoWriter(args.movie, cv2.VideoWriter_fourcc('M','J','P','G'), args.fps, (128*args.scaleup,128*args.scaleup)) \
            if args.movie is not None  else None

    # We'll use clock time (instead of event time) for speed
    times = np.zeros((128,128))

    # Start with an empty image
    image = np.zeros((128,128,3)).astype('uint8')

    while(True):

        # Get events from DVS, storing times and pixels
        while edvs.hasNext():
            x,y, p, t = edvs.next()
            image[x,y] = (0,255,0) if p == -1 else (0,0,255)
            times[x,y] = t

        # Zero out pixels with events older than a certain time before now
        image[(time() -times) > args.interval] = 0

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

    edvs.stop()

    thread.join()

if __name__ == '__main__':

    main()

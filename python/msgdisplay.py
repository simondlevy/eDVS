#!/usr/bin/env python3
'''
Simple demo of the iniVation eDVS using OpenCV

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import cv2
import numpy as np
import argparse
import serial

EOM = 200

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default='/dev/ttyACM0' , help="Port (/dev/ttyACM0, COM5, etc.")
    parser.add_argument("-b", "--baud", default=115200, type=int, help="Baud rate")
    parser.add_argument("-i", "--interval", default=0.02, type=float, help="Fade-out interval for events")
    parser.add_argument("-f", "--fps", default=100, type=int, help="Dispaly frames per second")
    parser.add_argument("-s", "--scaleup", default=4, type=int, help="Scale-up factor")
    parser.add_argument("-m", "--movie", default=None, help="Movie file name")
    args = parser.parse_args()

    # Create a video file to save the movie if indicated
    out = cv2.VideoWriter(args.movie, cv2.VideoWriter_fourcc('M','J','P','G'), args.fps, (128*args.scaleup,128*args.scaleup)) \
            if args.movie is not None  else None

    # Track time so we can stop displaying old events
    counts = np.zeros((128,128)).astype('uint8')

    # Start with an empty image
    image = np.zeros((128,128,3)).astype('uint8')

    # Compute number of iterations before events should disappear, based on 1msec display assumption
    ageout = int(args.interval * 1000)

    port = serial.Serial(args.port, args.baud)

    while(True):

        val = ord(port.read())

        if val == 255:
            val = -1

        print('\n' if val == EOM else val, end=' ')

        '''
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
    '''

if __name__ == '__main__':

    main()

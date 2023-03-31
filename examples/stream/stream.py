#!/usr/bin/python3
'''
Display events of the iniVation Mini eDVS connected to a microcontroller

Copyright (C) 2023 Simon D. Levy

MIT License
'''

import cv2
import numpy as np
import argparse
import serial
from time import time

def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('-p', '--port', default='/dev/ttyACM0',
                           help='Port (/dev/ttyACM0, COM5, etc.')
    argparser.add_argument('-b', '--baud', default=115200, type=int,
                           help='Baud rate')
    argparser.add_argument('-m', '--maxbuf', default=4096, type=int,
                           help='Maximum buffer size')
    argparser.add_argument('-t', '--timeout', default=.01, type=float,
                           help='Timeout for serial read (sec)')
    argparser.add_argument('-s', '--scaleup', default=2, type=int,
                           help='Scale-up factor')
    argparser.add_argument('-f', '--filename', default='events.dat', 
                           help='binary file in which to save events')

    args = argparser.parse_args()

    with serial.Serial(args.port, args.baud, timeout=args.timeout) as port:

        time_prev = 0
        event_count = 0
        frame_count = 0

        outfile = None if args.filename is None else open(args.filename, 'wb')

        while (True):

            try:

                # Read raw bytes from serial and convert them to signed eight-bit ints
                data = np.frombuffer(port.read(args.maxbuf), dtype=np.int8)

                x = data[::2]
                y = data[1::2]

                # Keep X and Y arrays the same size
                n = min(len(x), len(y))

                # Record to file if indicated
                if outfile is not None:
                    for k in range(n):
                        outfile.write(x[k])
                        outfile.write(y[k])

                # Report event count each second
                event_count += n
                if time() - time_prev > 1:
                    if time_prev > 0:
                        print('%6d events per second; %d frames per second; %d events per frame' %
                              (event_count, frame_count, event_count/frame_count))
                    time_prev = time()
                    event_count = 0
                    frame_count = 0

                # Avoid displaying empty buffer
                if n > 0:

                    # Keep X and Y coordinates same size
                    x = x[:n]
                    y = y[:n]

                    # Fill image with white pixels at event locations
                    image = np.zeros((128, 128)).astype('uint8')
                    image[x,y] = 255

                    # Scale up the image for visibility
                    bigimage = cv2.resize(image, (128*args.scaleup, 128*args.scaleup))

                    # Display the upscaled image
                    cv2.imshow(args.port, bigimage)

                    # Quit on ESCape
                    if cv2.waitKey(1) == 27:
                        break

                    frame_count += 1

            except KeyboardInterrupt:
                break

        cv2.destroyAllWindows()

        if outfile is not None:
            outfile.close()


main()

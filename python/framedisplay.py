#!/usr/bin/python3
'''
Simple demo of the iniVation Mini eDVS using frames

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import cv2
import numpy as np
import argparse
import serial

MAX_EVENTS_PER_FRAME = 5000

EOM = 200

def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument("-p", "--port", default='/dev/ttyACM0',
                           help="Port (/dev/ttyACM0, COM5, etc.")
    argparser.add_argument("-b", "--baud", default=921600, type=int,
                           help="Baud rate")
    argparser.add_argument("-t", "--timeout", default=.01, type=float,
                           help="Timeout for serial read (sec)")
    argparser.add_argument("-s", "--scaleup", default=4, type=int,
                           help="Scale-up factor")

    args = argparser.parse_args()

    port = serial.Serial(args.port, args.baud, timeout=args.timeout)

    while(True):

        try:

            # Read raw bytes from serial and convert them to signed eight-bit ints
            data = np.frombuffer(port.read(5000), dtype=np.int8)

            # Separate X and Y components
            x = data[::2]
            y = data[1::2]

            # Keep X and Y arrays the same size
            n = min(len(x), len(y))
            x = x[:n]
            y = y[:n]

            # Fill image with white pixels at event locations
            image = np.zeros((128, 128)).astype('uint8')
            image[x,y] = 255

            # Scale up the image for visibility
            bigimage = cv2.resize(image, (128*args.scaleup, 128*args.scaleup))

            # Display the upscaled image
            cv2.imshow('Mini eDVS', bigimage)

            # Quit on ESCape
            if cv2.waitKey(1) == 27:
                break

        except KeyboardInterrupt:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':

    main()

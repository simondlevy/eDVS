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
    argparser.add_argument("-s", "--scaleup", default=4, type=int,
                           help="Scale-up factor")

    args = argparser.parse_args()

    port = serial.Serial(args.port, args.baud)

    idx = 0

    while(True):

        try:

            # Read raw bytes from serial and convert them to unsigned eight-bit ints
            data = np.frombuffer(port.read(5000), dtype=np.uint8)
 
            # Find the positions of the polarity values (+1, 255=-1)
            polpos = np.logical_or(data == 1, data == 255)
            
            # Use the position of the first polarity value as a sentinel
            beg = np.argmax(polpos) + 1
            events = data[beg:]
            x = np.array(events[::3])
            y = np.array(events[1::3])

            # Replace stray polarity values with 0
            x[x>127] = 0
            y[y>127] = 0

            # Handle off-by-one size mismatch
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
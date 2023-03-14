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

            data = np.frombuffer(port.read(5000), dtype=np.uint8)
 
            polpos = np.logical_or(data == 1, data == 255)
            
            beg = np.argmax(polpos) + 1

            end = 5000 - np.argmax(polpos[::-1])

            events = data[beg:end]

            x = np.array(events[::3])
            y = np.array(events[1::3])

            x[x>127] = 0
            y[y>127] = 0

            n = min(len(x), len(y))

            x = x[:n]
            y = y[:n]

            image = np.zeros((128, 128)).astype('uint8')

            image[x,y] = 255

            # Scale up the image for visibility
            bigimage = cv2.resize(image, (128*args.scaleup, 128*args.scaleup))

            # Display the large color image
            cv2.imshow('Mini eDVS', bigimage)

            # Quit on ESCape
            if cv2.waitKey(1) == 27:
                break

        except KeyboardInterrupt:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':

    main()

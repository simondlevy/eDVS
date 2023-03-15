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
import time

BAUD = 921600

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

    count = 0

    prev = 0

    while(True):

        try:

            byte = ord(port.read(1))

            count += 1

            curr = time.time()

            if curr - prev > 1.0:

                prev = curr
                print(count)
                count = 0

        except KeyboardInterrupt:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':

    main()

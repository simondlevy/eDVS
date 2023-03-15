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

    byte_count = 0

    time_prev = 0

    while(True):

        try:

            byte = ord(port.read(1))

            byte_count += 1

            time_curr = time.time()

            if time_curr - time_prev > 1.0:

                time_prev = time_curr

                if byte_count > 3:
                    print('%d events per second' % (byte_count//3))

                byte_count = 0


        except KeyboardInterrupt:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':

    main()

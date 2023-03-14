#!/usr/bin/python3
'''
Copyright (C) 2023 Simon D. Levy

Read and display JPEG-compressed event images over USB

MIT License
'''

import serial
import numpy as np
import cv2
import argparse


def display(img_data, scaleup, delay):

    quit = False

    jpg_as_np = np.frombuffer(img_data, dtype=np.uint8)

    image = cv2.imdecode(jpg_as_np, flags=cv2.IMREAD_GRAYSCALE)

    if image is not None:

        bigimage = cv2.resize(image, (128*scaleup, 128*scaleup))

        cv2.imshow('image', bigimage)

        quit = cv2.waitKey(delay) == 27  # ESC

    return quit


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument("-p", "--port", default='/dev/ttyACM0',
                           help="Port (/dev/ttyUSB0, COM5, etc.")
    argparser.add_argument("-b", "--baud", default=115200, type=int,
                           help="Baud rate")
    argparser.add_argument("-s", "--scaleup", default=2, type=int,
                           help="Scale-up factor")
    argparser.add_argument("-d", "--delay", default=15, type=int,
                           help="Millsecond delay between frames")

    args = argparser.parse_args()

    # Connect to Teensy
    port = serial.Serial(args.port, args.baud, timeout=0.02)

    prev = 0

    buf = []

    try:

        while(True):

            # img_data = port.read(10_000)
            data = port.read()

            if len(data) > 0:

                byte = ord(data)

                if byte == 0xD8 and prev == 0xFF:

                    if len(buf) > 1000:

                        if display(bytes(buf), args.scaleup, args.delay):
                            break

                    buf = [prev, byte]

                else:
                    buf += [byte]

                prev = byte


    except KeyboardInterrupt:

        port.close()


main()

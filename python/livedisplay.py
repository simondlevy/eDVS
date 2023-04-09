#!/usr/bin/python3
'''
Experiments with DVS filtering

Copyright (C) 2023 Simon D. Levy

MIT License
'''

from edvs import EDVS
from threading import Thread
import cv2
import numpy as np
import argparse
from time import time, sleep

from filters.dvsnoise import SpatioTemporalCorrelationFilter
from filters.knoise import OrderNbackgroundActivityFilter


class PassThruFilter:

    def check(self, e):

        return True


def add_events_per_second(bigimage, xpos, value):

    cv2.putText(bigimage,
                '%d events/second' % value,
                (xpos, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,            # scale
                (0, 255, 255),  # color
                1,              # thickness
                2)              # line type

def new_image():

    return np.zeros((128, 256, 3), dtype=np.uint8)


def polarity2color(x, y, p, args):

    return (((0, 0, 255) if p else (0, 255, 0))
            if args.color else (255, 255, 255))

def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('-p', '--port', default='/dev/ttyUSB0',
                           help='Port (/dev/ttyUSB0, COM5, etc.')

    argparser.add_argument('-b', '--baud', default=2000000, type=int,
                           help='Baud rate')

    argparser.add_argument('-e', '--event-format', type=int, default=4,
                           choices=(0, 2, 3, 4),
                           help='Event format')

    argparser.add_argument('-f', '--fps', type=int, default=30,
                           help='Frame rate per second for display')

    argparser.add_argument('-c', '--color', action='store_true',
                           help='Display in color')

    argparser.add_argument('-d', '--denoising', default='none',
                           choices=('dvsknoise', 'knoise', 'none'),
                           help='Denoising filter choice')

    argparser.add_argument('-t', '--maxtime', type=float,
                           help='Maximum time to play in seconds')

    argparser.add_argument('-v', '--video', default=None,
                           help='Name of video file to save')

    argparser.add_argument('-s', '--scaleup', type=int, default=2,
                           help='Scale-up factor for display')

    args = argparser.parse_args()

    # Connect to sensor
    edvs = EDVS(args.port, args.baud, event_format=args.event_format)

    # Display firmware version
    print(edvs.version())

    # Start sensor on its own thread
    thread = Thread(target=edvs.start)
    thread.daemon = True
    thread.start()

    try:

        while True:

            # Get events from DVS
            if edvs.hasNext():
                x, y, p = edvs.next()
                print(x, y, p)

            # Yield to sensor thread
            sleep(.0001)

    except KeyboardInterrupt:

        edvs.reset()
        exit(0)

main()

#!/usr/bin/python3
'''
Simple demo of the iniVation Mini eDVS via FTDI adapter

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from edvs import EDVS
from threading import Thread
import cv2
import numpy as np
import argparse
import traceback

from utils import polarity2color, parse_args, close_video
from utils import Display


def run(edvs, args, denoise, video_out):

    # Create a display window for the events
    display = Display('mini-eDVS')

    # Display firmware version
    print(edvs.version())

    # Track time so we can stop displaying old events
    raw_counts = np.zeros((128, 128)).astype('uint8')
    flt_counts = np.zeros((128, 128)).astype('uint8')

    # Compute number of iterations before events should disappear, based on
    # 1msec display assumption
    ageout = int(1./args.fps * 1000)

    # Start sensor on its own thread
    thread = Thread(target=edvs.start)
    thread.daemon = True
    thread.start()

    while True:

        # Get events from DVS
        while edvs.hasNext():

            e = edvs.next()

            # Add event to unfiltered image
            display.raw_total += 1
            display.raw_image[e.x, e.y] = polarity2color(e, args)

            # Add event to filtered image if event passes the filter
            if denoise.check(e):
                display.flt_image[e.x, e.y] = polarity2color(e, args)
                display.flt_total += 1
                flt_counts[e.x, e.y] = 1

            raw_counts[e.x, e.y] = 1

        # Zero out events older than a certain time before now
        display.raw_image[raw_counts == ageout] = 0
        raw_counts[raw_counts == ageout] = 0
        display.flt_image[flt_counts == ageout] = 0
        flt_counts[flt_counts == ageout] = 0

        # Increase age for events
        raw_counts[raw_counts > 0] += 1
        flt_counts[flt_counts > 0] += 1

        if not display.show(args, video_out):
            break

    cv2.destroyAllWindows()

    close_video(video_out)

    edvs.stop()

    thread.join()


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('-p', '--port', default='/dev/ttyUSB0',
                           help='Port (/dev/ttyUSB0, COM5, etc.')

    argparser.add_argument('-b', '--baud', default=2000000, type=int,
                           help='Baud rate')

    argparser.add_argument('-e', '--event-format', type=int, default=0,
                           choices=(0, 2, 3, 4),
                           help='Event format')

    args, denoise, video_out = parse_args(argparser)

    # Connect to sensor
    edvs = EDVS(args.port, args.baud, event_format=args.event_format)

    try:
        run(edvs, args, denoise, video_out)

    # Stop streaming on error
    except Exception:
        traceback.print_exc()
        edvs.reset()
        exit(0)


if __name__ == '__main__':

    main()

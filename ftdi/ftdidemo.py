#!/usr/bin/python3
'''
Simple demo of the iniVation Mini eDVS via FTDI adapter

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from edvs import EDVS
from threading import Thread
import numpy as np
import argparse
import traceback

from display import parse_args, Display


def init_counts():
    return np.zeros((128, 128)).astype('uint8')


def update_counts(counts, e):
    counts[e.y, e.x] = 1


def update_image_from_counts(image, counts, ageout):
    image[counts == ageout] = 0
    counts[counts == ageout] = 0
    counts[counts > 0] += 1


def run(edvs, display, fps):

    # Display firmware version
    print(edvs.version())

    # Track time so we can stop displaying old events
    raw_counts = init_counts()
    flt_counts = init_counts()

    # Compute number of iterations before events should disappear, based on
    # 1msec display assumption
    ageout = int(1./fps * 1000)

    # Start sensor on its own thread
    thread = Thread(target=edvs.start)
    thread.daemon = True
    thread.start()

    while True:

        # Get events from DVS
        while edvs.hasNext():

            e = edvs.next()

            # Update event counts for fade-out
            update_counts(raw_counts, e)

            # Display.addEvent() returns True iff event passed denoising filter
            if display.addEvent(e):
                update_counts(flt_counts, e)

        # Zero out events older than a certain time before now
        update_image_from_counts(display.raw_image, raw_counts, ageout)
        update_image_from_counts(display.flt_image, flt_counts, ageout)

        if not display.show():
            break

    display.close()

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

    argparser.add_argument('-k', '--kfps', default=30, type=int,
                           help='Frames Per Second')

    args = parse_args(argparser)

    # Connect to sensor
    edvs = EDVS(args.port, args.baud, event_format=args.event_format)

    # Create a display window for the events
    display = Display('mini-eDVS', args)

    try:
        run(edvs, display, args.kfps)

    # Stop streaming on error
    except Exception:
        traceback.print_exc()
        edvs.reset()
        exit(0)


if __name__ == '__main__':

    main()

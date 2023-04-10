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
from time import time
import traceback

from utils import polarity2color, parse_args, show_big_image, close_video, new_image

def run(edvs, args, denoise, video_out):

    # Display firmware version
    print(edvs.version())

    # Track time so we can stop displaying old events
    raw_counts = np.zeros((128, 128)).astype('uint8')
    flt_counts = np.zeros((128, 128)).astype('uint8')

    # Start with empty images
    raw_image = new_image()
    flt_image = new_image()

    raw_per_second = 0
    flt_per_second = 0

    # Helps group events into frames
    frames_this_second = 0

    # Supports the -t (quit after specified time) option
    total_time = 0

    # Supports statistics reporting
    raw_total = 0
    flt_total = 0
    raw_per_second = 0
    flt_per_second = 0

    # Compute number of iterations before events should disappear, based on
    # 1msec display assumption
    ageout = int(1./args.fps * 1000)

    # Start sensor on its own thread
    thread = Thread(target=edvs.start)
    thread.daemon = True
    thread.start()

    time_start = time()

    while True:

        # Get events from DVS
        while edvs.hasNext():

            e = edvs.next()

            raw_total += 1

            raw_image[e.x, e.y] = polarity2color(e, args)
            raw_counts[e.x, e.y] = 1

            # Add event to filtered image if event passes the filter
            if denoise.check(e):
                flt_image[e.x, e.y] = polarity2color(e, args)
                flt_counts[e.x, e.y] = 1
                flt_total += 1

        # Zero out events older than a certain time before now
        raw_image[raw_counts == ageout] = 0
        raw_counts[raw_counts == ageout] = 0
        flt_image[flt_counts == ageout] = 0
        flt_counts[flt_counts == ageout] = 0

        # Increase age for events
        raw_counts[raw_counts > 0] += 1
        flt_counts[flt_counts > 0] += 1

        if not show_big_image(
                'mini-eDVS', 
                args.scaleup, 
                raw_image, 
                raw_per_second,
                flt_image,
                flt_per_second,
                video_out):
            break

        # Update events-per-second totals every second
        frames_this_second += 1
        if frames_this_second == args.fps:

            # Quit after specified time if indicated
            total_time += 1
            if (args.maxtime is not None and
                    total_time >= args.maxtime):
                break

            # Update stats for reporting
            raw_per_second = raw_total
            flt_per_second = flt_total
            raw_total = 0
            flt_total = 0
            frames_this_second = 0

        # Quit after specified time if indicated
        if args.maxtime is not None and time() - time_start >= args.maxtime:
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
    except Exception as e:
        traceback.print_exc()
        edvs.reset()
        exit(0)



if __name__ == '__main__':

    main()

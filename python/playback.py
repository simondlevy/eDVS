#!/usr/bin/python3
'''
Experiments with DVS filtering

Copyright (C) 2023 Simon D. Levy

MIT License
'''

from dv import AedatFile
import numpy as np
import argparse
import cv2
from time import time

from filters.dvsnoise import SpatioTemporalCorrelationFilter
from filters.knoise import OrderNbackgroundActivityFilter

from utils import PassThruFilter, add_events_per_second, polarity2color
from utils import parse_args, show_big_image, close_video


def new_image():

    return np.zeros((128, 256, 3), dtype=np.uint8)


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    args, video_out = parse_args(argparser)

    image = new_image()

    time_prev = 0

    filt = (OrderNbackgroundActivityFilter()
            if args.denoising == 'knoise'
            else SpatioTemporalCorrelationFilter()
            if args.denoising == 'dvsnoise'
            else PassThruFilter())

    # Helps group events into frames
    frames_this_second = 0

    # Supports the -t (quit after specified time) option
    total_time = 0

    # Supports statistics reporting
    raw_total = 0
    filt_total = 0
    raw_per_second = 0
    filt_per_second = 0

    with AedatFile(args.filename) as f:

        try:

            for e in f['events']:

                # Add event to unfiltered image
                image[e.y, e.x] = polarity2color(e.x, e.y, e.polarity, args)

                raw_total += 1

                # Add event to filtered image if event passes the filter
                if filt.check(e):
                    image[e.y, e.x + 128] = \
                            polarity2color(e.x, e.y, e.polarity, args)
                    filt_total += 1

                # Update images periodically
                if time() - time_prev > 1./args.fps:

                    time_prev = time()

                    # Make big image from raw/filtered image frame
                    bigimage = cv2.resize(image,
                                          (image.shape[1]*args.scaleup,
                                           image.shape[0]*args.scaleup))

                    # Draw a line down the middle of the big image to separate
                    # raw from filtered
                    bigimage[:, 128*args.scaleup] = 255

                    # Report events per second every second
                    if raw_per_second > 0:
                        add_events_per_second(bigimage, 50, raw_per_second)
                        add_events_per_second(bigimage, 300, filt_per_second)

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
                        filt_per_second = filt_total
                        raw_total = 0
                        filt_total = 0
                        frames_this_second = 0

                    if not show_big_image(args.filename, bigimage, video_out):
                        break

                    # Start over with a new empty frame
                    image = new_image()

            close_video(video_out)

        except KeyboardInterrupt:

            close_video(video_out)

            exit(0)


main()

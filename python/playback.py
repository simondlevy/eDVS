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
from utils import parse_args, show_big_image, close_video, new_image


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    args, video_out = parse_args(argparser)

    raw_image = new_image()
    flt_image = new_image()

    time_prev = 0

    denoise = (OrderNbackgroundActivityFilter()
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
    flt_total = 0
    raw_per_second = 0
    flt_per_second = 0

    with AedatFile(args.filename) as f:

        try:

            for e in f['events']:

                # Add event to unfiltered image
                raw_image[e.y, e.x] = polarity2color(e, args)

                raw_total += 1

                # Add event to filtered image if event passes the filter
                if denoise.check(e):
                    flt_image[e.y, e.x] = polarity2color(e, args)
                    flt_total += 1

                # Update images periodically
                if time() - time_prev > 1./args.fps:

                    time_prev = time()

                    if not show_big_image(
                            args.filename, 
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

                    # Start over with a new empty frame
                    raw_image = new_image()
                    flt_image = new_image()

            close_video(video_out)

        except KeyboardInterrupt:

            close_video(video_out)

            exit(0)


main()

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

from utils import PassThruFilter, add_events_per_second, polarity2color
from utils import parse_args, show_big_image, close_video, new_image
from utils import Display


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    args, denoise, video_out = parse_args(argparser)

    display = Display()

    time_prev = 0

    with AedatFile(args.filename) as f:

        try:

            for e in f['events']:

                # Add event to unfiltered image
                display.raw_image[e.y, e.x] = polarity2color(e, args)

                display.raw_total += 1

                # Add event to filtered image if event passes the filter
                if denoise.check(e):
                    display.flt_image[e.y, e.x] = polarity2color(e, args)
                    display.flt_total += 1

                # Update images periodically
                if time() - time_prev > 1./args.fps:

                    time_prev = time()

                    if not show_big_image(
                            args.filename, 
                            args.scaleup, 
                            display.raw_image, 
                            display.raw_per_second,
                            display.flt_image,
                            display.flt_per_second,
                            video_out):
                        break

                    # Update events-per-second totals every second
                    display.frames_this_second += 1
                    if display.frames_this_second == args.fps:

                        # Quit after specified time if indicated
                        display.total_time += 1
                        if (args.maxtime is not None and
                                display.total_time >= args.maxtime):
                            break

                        # Update stats for reporting
                        display.raw_per_second = display.raw_total
                        display.flt_per_second = display.flt_total
                        display.raw_total = 0
                        display.flt_total = 0
                        display.frames_this_second = 0

                    # Start over with a new empty frame
                    display.raw_image = new_image()
                    display.flt_image = new_image()

            close_video(video_out)

        except KeyboardInterrupt:

            close_video(video_out)

            exit(0)


main()

#!/usr/bin/python3
'''
Experiments with DVS filtering

Copyright (C) 2023 Simon D. Levy

MIT License
'''

from dv import AedatFile
import argparse
from time import time

from utils import polarity2color
from utils import parse_args, close_video, new_image
from utils import Display


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    args, denoise, video_out = parse_args(argparser)

    display = Display(args.filename)

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

                    if not display.show(args, video_out):
                        break

                    # Start over with a new empty frame
                    display.raw_image = new_image()
                    display.flt_image = new_image()

            close_video(video_out)

        except KeyboardInterrupt:

            close_video(video_out)

            exit(0)


main()

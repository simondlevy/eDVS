#!/usr/bin/python3
'''
Experiments with DVS filtering

Copyright (C) 2023 Simon D. Levy

MIT License
'''

from dv import AedatFile
import argparse
from time import time

from utils import parse_args, close_video, new_image
from utils import Display


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    args, denoise, video_out = parse_args(argparser)

    display = Display(args.filename, denoise, args)

    time_prev = 0

    with AedatFile(args.filename) as f:

        try:

            for e in f['events']:

                display.addEvent(e)

                # Update images periodically
                if time() - time_prev > 1./args.fps:

                    time_prev = time()

                    if not display.show():
                        break

                    # Start over with a new empty frame
                    display.raw_image = new_image()
                    display.flt_image = new_image()

            close_video(video_out)

        except KeyboardInterrupt:

            close_video(video_out)

            exit(0)


main()

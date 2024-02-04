#!/usr/bin/python3
'''
Plays back an AEDAT4 file with filtering and optical flow

Copyright (C) 2023 Simon D. Levy

MIT License
'''

from dv import AedatFile
import argparse
from time import time

from display import parse_args, Display


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    args = parse_args(argparser)

    display = Display(args.filename, args)

    time_prev = 0

    with AedatFile(args.filename) as f:

        try:

            for e in f['events']:

                display.addEvent(e)

                # Update images periodically
                if time() - time_prev > 1./args.rate:

                    time_prev = time()

                    if not display.show():
                        break

                    display.report()

                    # Start over with a new empty frame
                    display.clear()

            display.close()

        except KeyboardInterrupt:

            display.close()

            exit(0)


main()

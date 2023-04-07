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


class _PassThruFilter:

    def check(self, e):

        return True


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    argparser.add_argument('-s', '--scaleup', type=int, default=2,
                           help='Scale-up factor for display')

    argparser.add_argument('-r', '--rate', type=int, default=30,
                           help='Frame rate per second for display')

    argparser.add_argument('-f', '--filter', default='none',
                           choices=('dvsknoise', 'knoise', 'none'),
                           help='Filter choice')

    args = argparser.parse_args()

    image = np.zeros((128, 256))

    time_prev = 0



    filt = (OrderNbackgroundActivityFilter() if args.filter == 'knoise'
            else SpatioTemporalCorrelationFilter() if args.filter == 'dvsnoise' 
            else _PassThruFilter())

    with AedatFile(args.filename) as f:

        try:

            for e in f['events']:

                # Add event to unfiltered image
                image[e.y, e.x] = 255

                # Add event to filtered image if event passes the filter
                if filt.check(e):
                    image[e.y, e.x + 128] = 255

                # Update images periodically
                if time() - time_prev > 1./args.rate:

                    time_prev = time()

                    bigimage = cv2.resize(image,
                                          (image.shape[1]*args.scaleup,
                                           image.shape[0]*args.scaleup))

                    bigimage[:, 128*args.scaleup] = 255

                    cv2.imshow(args.filename, bigimage)

                    image = np.zeros((128, 256))

                    if cv2.waitKey(1) == 27:
                        break

        except KeyboardInterrupt:

            exit(0)


main()

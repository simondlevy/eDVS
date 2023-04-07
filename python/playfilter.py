#!/usr/bin/python3
'''
Experiments with DVS filtering

Copyright (C) 2023 Simon D. Levy

MIT License
'''

from dv import AedatFile
import aedat
import numpy as np
import argparse
import cv2
from time import time

from filters.dvsnoise import SpatioTemporalCorrelationFilter
from filters.knoise import OrderNbackgroundActivityFilter


class _PassThruFilter:

    def check(self, e):

        return True


def _show_events_per_second(bigimage, xpos, value):

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (xpos, 25)
    fontScale              = 0.5 
    fontColor              = (255, 255, 255)
    thickness              = 1
    lineType               = 2

    cv2.putText(bigimage,
                '%d events/second' % value,
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)



def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    argparser.add_argument('-s', '--scaleup', type=int, default=2,
                           help='Scale-up factor for display')

    argparser.add_argument('-f', '--fps', type=int, default=30,
                           help='Frame rate per second for display')

    argparser.add_argument('-d', '--denoising', default='none',
                           choices=('dvsknoise', 'knoise', 'none'),
                           help='Denoising filter choice')

    args = argparser.parse_args()

    image = np.zeros((128, 256))

    time_prev = 0

    # Get final timestamp
    decoder = aedat.Decoder(args.filename)
    packets = [packet for packet in decoder]
    last_timestamp = packets[-1]['events'][-1][0]

    filt = (OrderNbackgroundActivityFilter(last_timestamp) if args.denoising == 'knoise'
            else SpatioTemporalCorrelationFilter() if args.denoising == 'dvsnoise' 
            else _PassThruFilter())

    raw_total = 0
    filt_total = 0
    frame_count = 0
    raw_per_second = 0
    filt_per_second = 0

    with AedatFile(args.filename) as f:

        try:

            for e in f['events']:

                # Add event to unfiltered image
                image[e.y, e.x] = 255

                raw_total += 1

                # Add event to filtered image if event passes the filter
                if filt.check(e):
                    image[e.y, e.x + 128] = 255
                    filt_total += 1

                # Update images periodically
                if time() - time_prev > 1./args.fps:

                    time_prev = time()

                    bigimage = cv2.resize(image,
                                          (image.shape[1]*args.scaleup,
                                           image.shape[0]*args.scaleup))

                    bigimage[:, 128*args.scaleup] = 255

                    frame_count += 1

                    if raw_per_second > 0:
                        _show_events_per_second(bigimage, 50, raw_per_second)
                        _show_events_per_second(bigimage, 300, filt_per_second)

                    # Update events-per-second totals every second
                    if frame_count == args.fps:

                        raw_per_second = raw_total
                        filt_per_second = filt_total

                        raw_total = 0
                        filt_total = 0
                        frame_count = 0

                    cv2.imshow(args.filename, bigimage)

                    image = np.zeros((128, 256))


                    if cv2.waitKey(1) == 27:
                        break

        except KeyboardInterrupt:

            exit(0)


main()

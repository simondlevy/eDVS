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


def _show_events_per_second(bigimage, xpos, value):

    cv2.putText(bigimage,
                '%d events/second' % value,
                (xpos, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,            # scale
                (0, 255, 255),  # color
                1,              # thickness
                2)              # line type

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

    argparser.add_argument('-t', '--maxtime', type=float,
                           help='Maximum time to play in seconds')

    argparser.add_argument('-v', '--video', default=None,
                           help='Name of video file to save')

    args = argparser.parse_args()

    image = np.zeros((128, 256), dtype=np.uint8)

    time_prev = 0

    filt = (OrderNbackgroundActivityFilter() if args.denoising == 'knoise'
            else SpatioTemporalCorrelationFilter() if args.denoising == 'dvsnoise' 
            else _PassThruFilter())

    # Helps group events into frames
    frames_this_second = 0

    # Supports the -t (quit after specified time) option
    total_time = 0

    # Supports statistics reporting
    raw_total = 0
    filt_total = 0
    raw_per_second = 0
    filt_per_second = 0
    
    # Open video output file if indicated
    video_out = (cv2.VideoWriter(args.video,
                          cv2.VideoWriter_fourcc('M','J','P','G'),
                          30,
                          (args.scaleup * 256, args.scaleup * 128))
           if args.video is not None else None)

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

                    # Make big image from raw/filtered image frame
                    bigimage = cv2.resize(image,
                                          (image.shape[1]*args.scaleup,
                                           image.shape[0]*args.scaleup))

                    # Draw a line down the middle of the big image to separate
                    # raw from filtered
                    bigimage[:, 128*args.scaleup] = 255

                    # Convert big image to color
                    bigimage = cv2.cvtColor(bigimage, cv2.COLOR_GRAY2BGR)

                     # Report events per second every second
                    if raw_per_second > 0:
                        _show_events_per_second(bigimage, 50, raw_per_second)
                        _show_events_per_second(bigimage, 300, filt_per_second)

                    # Update events-per-second totals every second
                    frames_this_second += 1
                    if frames_this_second == args.fps:

                        # Quit after specified time if indicated
                        total_time += 1
                        if args.maxtime is not None and total_time >= args.maxtime:
                            break

                        # Update stats for reporting
                        raw_per_second = raw_total
                        filt_per_second = filt_total
                        raw_total = 0
                        filt_total = 0
                        frames_this_second = 0

                    # Show big image, quitting on ESC
                    cv2.imshow(args.filename, bigimage)
                    if cv2.waitKey(1) == 27:
                        break

                    # Save current big image frame if indicated
                    if video_out is not None:
                        video_out.write(bigimage, cv2.COLOR_GRAY2BGR)

                    # Start over with a new empty frame
                    image = np.zeros((128, 256), dtype=np.uint8)

            if video_out is not None:
                video_out.release()

        except KeyboardInterrupt:

            if video_out is not None:
                video_out.release()

            exit(0)


main()

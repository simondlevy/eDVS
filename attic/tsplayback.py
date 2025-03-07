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

from filters.dvsnoise import SpatioTemporalCorrelationFilter
from filters.knoise import Knoise


class PassThruFilter:

    def check(self, e):

        return True


def add_events_per_second(bigimage, xpos, value):

    cv2.putText(bigimage,
                '%d events/second' % value,
                (xpos, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,            # scale
                (0, 255, 255),  # color
                1,              # thickness
                2)              # line type

def new_image():

    return np.zeros((128, 256, 3), dtype=np.uint8)

def polarity2color(e, args):

    return (((0, 0, 255) if e.polarity else (0, 255, 0))
            if args.color else (255, 255, 255))

def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    argparser.add_argument('-f', '--fps', type=int, default=30,
                           help='Frame rate per second for display')

    argparser.add_argument('-c', '--color', action='store_true',
                           help='Display in color')

    argparser.add_argument('-d', '--denoising', default='none',
                           choices=('dvsknoise', 'knoise', 'none'),
                           help='Denoising filter choice')

    argparser.add_argument('-t', '--maxtime', type=float,
                           help='Maximum time to play in seconds')

    argparser.add_argument('-v', '--video', default=None,
                           help='Name of video file to save')

    argparser.add_argument('-s', '--scaleup', type=int, default=2,
                           help='Scale-up factor for display')

    args = argparser.parse_args()

    image = new_image()

    filt = (Knoise() if args.denoising == 'knoise'
            else SpatioTemporalCorrelationFilter() if args.denoising == 'dvsnoise' 
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

    # Open video output file if indicated
    video_out = (cv2.VideoWriter(args.video,
                                 cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                 30,
                                 (args.scaleup * 256, args.scaleup * 128))
                 if args.video is not None else None)

    with AedatFile(args.filename) as f:

        try:

            timestamp_prev = 0

            for e in f['events']:

                # Add event to unfiltered image
                image[e.y, e.x] = polarity2color(e, args)

                raw_total += 1

                # Add event to filtered image if event passes the filter
                if filt.check(e):
                    image[e.y, e.x+128] = polarity2color(e, args)
                    filt_total += 1

                # Update images periodically
                if e.timestamp - timestamp_prev > 1e6 / args.fps:

                    # Update events-per-second totals every second
                    frames_this_second += 1
                    if frames_this_second == args.fps:

                        # Quit after specified time if indicated
                        total_time += 1
                        if args.maxtime is not None:
                            if total_time >= args.maxtime:
                                break

                        # Update stats for reporting
                        raw_per_second = raw_total
                        filt_per_second = filt_total
                        raw_total = 0
                        filt_total = 0
                        frames_this_second = 0

                    # Make big image from raw/filtered image frame
                    bigimage = cv2.resize(image,
                                          (image.shape[1]*args.scaleup,
                                           image.shape[0]*args.scaleup))

                    # Draw a line down the middle of the big image to separate
                    # raw from filtered
                    bigimage[:, 128*args.scaleup] = 255

                    # Overlay events per second on big image every second
                    if raw_per_second > 0:
                        add_events_per_second(bigimage, 50, raw_per_second)
                        add_events_per_second(bigimage, 300, filt_per_second)

                    # Show big image, quitting on ESC
                    cv2.imshow(args.filename, bigimage)
                    if cv2.waitKey(1) == 27:
                        break

                    # Save current big image frame if indicated
                    if video_out is not None:
                        video_out.write(bigimage, cv2.COLOR_GRAY2BGR)

                    image = new_image()

                    timestamp_prev = e.timestamp

            if video_out is not None:
                video_out.release()

        except KeyboardInterrupt:

            if video_out is not None:
                video_out.release()

            exit(0)


main()

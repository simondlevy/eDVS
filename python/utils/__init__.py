'''
DVS utilities

Copyright (C) 2023 Simon D. Levy

MIT License
'''

import numpy as np
import cv2

from filters.dvsnoise import SpatioTemporalCorrelationFilter
from filters.knoise import OrderNbackgroundActivityFilter


class Display:

    def __init__(self):

        # Start with empty images
        self.raw_image = new_image()
        self.flt_image = new_image()

        # Helps group events into frames
        self.frames_this_second = 0

        # Supports the -t (quit after specified time) option
        self.total_time = 0

        # Supports statistics reporting
        self.raw_total = 0
        self.flt_total = 0
        self.raw_per_second = 0
        self.flt_per_second = 0


class PassThruFilter:

    def check(self, e):

        return True

def parse_args(argparser):

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

    denoise = (OrderNbackgroundActivityFilter()
               if args.denoising == 'knoise'
               else SpatioTemporalCorrelationFilter()
               if args.denoising == 'dvsnoise'
               else PassThruFilter())

    video_out = (cv2.VideoWriter(args.video,
                                 cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                 30,
                                 (args.scaleup * 256, args.scaleup * 128))
                 if args.video is not None else None)

    return args, denoise, video_out


def add_events_per_second(image, xpos, value):

    if value > 0:

        cv2.putText(image,
                    '%d events/second' % value,
                    (xpos, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,            # scale
                    (0, 255, 255),  # color
                    1,              # thickness
                    2)              # line type


def new_image():

    return np.zeros((128, 128, 3), dtype=np.uint8)


def polarity2color(e, args):

    return (((0, 0, 255) if e.polarity else (0, 255, 0))
            if args.color else (255, 255, 255))


def _enlarge(image, factor):

    return cv2.resize(image, (128*factor, 128*factor))

def show_big_image(name,
                   scaleup,
                   raw_image,
                   raw_per_second,
                   flt_image,
                   flt_per_second,
                   video_out):


    big_image = np.hstack((_enlarge(raw_image, scaleup), _enlarge(flt_image, scaleup)))

    # Draw a line down the middle of the big image to separate
    # raw from filtered
    big_image[:, 128*scaleup] = 255

    add_events_per_second(big_image, 50, raw_per_second)
    add_events_per_second(big_image, 300, flt_per_second)

    # Show big image, quitting on ESC
    cv2.imshow(name, big_image)
    if cv2.waitKey(1) == 27:
        return False

    # Save current big image frame if indicated
    if video_out is not None:
        video_out.write(big_image)

    return True


def close_video(video_out):
    if video_out is not None:
        video_out.release()

'''
DVS utilities

Copyright (C) 2023 Simon D. Levy

MIT License
'''

import numpy as np
import cv2


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

    # Open video output file if indicated
    video_out = (cv2.VideoWriter(args.video,
                                 cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                 30,
                                 (args.scaleup * 256, args.scaleup * 128))
                 if args.video is not None else None)

    return args, video_out


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


def polarity2color(x, y, p, args):

    return (((0, 0, 255) if p else (0, 255, 0))
            if args.color else (255, 255, 255))


def show_big_image(name, bigimage, video_out):

    # Show big image, quitting on ESC
    cv2.imshow(name, bigimage)
    if cv2.waitKey(1) == 27:
        return False

    # Save current big image frame if indicated
    if video_out is not None:
        video_out.write(bigimage)

    return True


def close_video(video_out):
    if video_out is not None:
        video_out.release()

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

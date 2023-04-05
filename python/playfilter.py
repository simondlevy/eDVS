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

from filters import SpatioTemporalCorrelationFilter

def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    argparser.add_argument('-s', '--scaleup', type=int, default=2,
                           help='Scale-up factor for display')

    argparser.add_argument('-f', '--fps', type=int, default=30,
                           help='Frames Per Second for display')

    args = argparser.parse_args()

    image = np.zeros((128, 256))

    time_prev = 0

    stcf = SpatioTemporalCorrelationFilter()

    with AedatFile(args.filename) as f:

        try:

            for e in f['events']:

                stcf.step(e)

                image[e.y, e.x] = 255

                if time() - time_prev > 1./args.fps:

                    time_prev = time()

                    bigimage = cv2.resize(image,
                                          (image.shape[1]*args.scaleup,
                                           image.shape[0]*args.scaleup))

                    bigimage[:,128*args.scaleup] = 255

                    cv2.imshow(args.filename, bigimage)

                    image = np.zeros((128, 256))

                    if cv2.waitKey(1) == 27:
                        break

        except KeyboardInterrupt:

            exit(0)


main()

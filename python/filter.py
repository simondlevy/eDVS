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

SCALEUP = 2

def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('filename')

    args = argparser.parse_args()

    image = np.zeros((128, 128))

    with AedatFile(args.filename) as f:

        try:

            for e in f['events']:

                image[e.y, e.x] = 255

                bigimage = cv2.resize(image, (128*SCALEUP, 128*SCALEUP))

                cv2.imshow(args.filename, bigimage)

                if cv2.waitKey(1) == 27:
                    break

        except KeyboardInterrupt:

            exit(0)

main()


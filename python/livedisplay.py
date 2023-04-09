#!/usr/bin/python3
'''
Simple demo of the iniVation Mini eDVS via FTDI adapter

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from edvs import EDVS
from threading import Thread
import cv2
import numpy as np
import argparse
from time import time

from utils import polarity2color


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('-p', '--port', default='/dev/ttyUSB0',
                           help='Port (/dev/ttyUSB0, COM5, etc.')

    argparser.add_argument('-b', '--baud', default=2000000, type=int,
                           help='Baud rate')

    argparser.add_argument('-e', '--event-format', type=int, default=4,
                           choices=(0, 2, 3, 4),
                           help='Event format')

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

    argparser.add_argument('-s', '--scaleup', default=2, type=int,
                           help='Scale-up factor')

    args = argparser.parse_args()

    # Connect to sensor
    edvs = EDVS(args.port, args.baud, event_format=args.event_format)

    # Display firmware version
    print(edvs.version())

    # Start sensor on its own thread
    thread = Thread(target=edvs.start)
    thread.daemon = True
    thread.start()

    # Track time so we can stop displaying old events
    counts = np.zeros((128, 128)).astype('uint8')

    # Start with an empty image
    image = np.zeros((128, 128, 3)).astype('uint8')

    # Compute number of iterations before events should disappear, based on
    # 1msec display assumption
    ageout = int(1./args.fps * 1000)

    # Open video output file if indicated
    video_out = (cv2.VideoWriter(args.video,
                                 cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                 30,
                                 (args.scaleup * 256, args.scaleup * 128))
                 if args.video is not None else None)

    time_start = time()

    while(True):

        # Get events from DVS
        while edvs.hasNext():

            x, y, p = edvs.next()

            image[x, y] = polarity2color(x, y, p == -1, args)

            counts[x, y] = 1

        # Zero out events older than a certain time before now
        image[counts == ageout] = 0
        counts[counts == ageout] = 0

        # Increase age for events
        counts[counts > 0] += 1

        # Scale up the image for visibility
        bigimage = cv2.resize(image, (128*args.scaleup, 128*args.scaleup))

        # Display the large color image
        cv2.imshow('Mini eDVS', bigimage)

        # Quit on ESCape
        if cv2.waitKey(1) == 27:
            break

        # Save current big image frame if indicated
        if video_out is not None:
            video_out.write(bigimage)

        # Quit after specified time if indicated
        if args.maxtime is not None and time() - time_start >= args.maxtime:
            break

    cv2.destroyAllWindows()

    if video_out is not None:
        video_out.release()

    edvs.stop()

    thread.join()


if __name__ == '__main__':

    main()

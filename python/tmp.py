#!/usr/bin/python3
'''
Simple demo of the iniVation Mini eDVS via FTDI adapter

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from newedvs import EDVS
from threading import Thread
import cv2
import numpy as np


def main():


    # Connect to sensor
    edvs = EDVS('/dev/ttyUSB0', 2000000)

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
    ageout = int(0.02 * 1000)

    while(True):

        # Get events from DVS
        while edvs.hasNext():
            x, y, p = edvs.next()
            image[x, y] = (255, 255, 255)
            counts[x, y] = 1

        # Zero out events older than a certain time before now
        image[counts == ageout] = 0
        counts[counts == ageout] = 0

        # Increase age for events
        counts[counts > 0] += 1

        # Scale up the image for visibility
        bigimage = cv2.resize(image, (256,256))

        # Display the large color image
        cv2.imshow('Mini eDVS', bigimage)

        # Quit on ESCape
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

    edvs.stop()

    thread.join()


if __name__ == '__main__':

    main()

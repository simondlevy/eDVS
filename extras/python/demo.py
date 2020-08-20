#!/usr/bin/env python3
'''
Simple demo of the IniVation eDVS using OpenCV

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from edvs import eDVS
from threading import Thread
from time import time
import cv2
import numpy as np

# Change this to match your com port (e.g., 'COM5')
PORT = '/dev/ttyUSB0'

# Events older than this time in seconds get zeroed-out
INTERVAL = 0.10

# Frame rate for saving movie
VIDEO_FPS = 100

# Scale-up factor for display
SCALEUP = 4

def main():

    edvs = eDVS(PORT)

    # Start sensor on its own thread
    thread = Thread(target=edvs.start)
    thread.daemon = True
    thread.start()

    # Create a video file to save the movie
    out = cv2.VideoWriter('movie.avi', cv2.VideoWriter_fourcc('M','J','P','G'), VIDEO_FPS, (128*SCALEUP,128*SCALEUP))

    while(True):

        # Zero out pixels with events older than a certain time before now
        edvs.events[(time() - edvs.times) > INTERVAL] = 0

        # Convert events to large color image
        image = np.zeros((128,128,3)).astype('uint8')
        image[edvs.events==+1,2] = 255
        image[edvs.events==-1,1] = 255
        image = cv2.resize(image, (128*SCALEUP,128*SCALEUP))

        # Write the color image to the video file
        out.write(image)

        # Display the large color image
        cv2.imshow('Mini eDVS', image)

        # Quit on ESCape
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

    edvs.stop()

    thread.join()

if __name__ == '__main__':

    main()

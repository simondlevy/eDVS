#!/usr/bin/env python3
'''
Gets four-byte messages from the eDVS USB adapter, converts them into events,
and displays them using OpenCV


Copyright (C) 2023 Simon D. Levy

MIT License
'''

import cv2
import numpy as np
import argparse
import serial

EOM = 200

# We implement a simple state machine for parsing four-byte messages (X, Y, P, EOM)
STATE_NONE   = 0
STATE_BEGIN  = 1
STATE_GET_X  = 2
STATE_GET_Y  = 3
STATE_GET_P  = 4

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default='/dev/ttyACM0' , help="Port (/dev/ttyACM0, COM5, etc.")
    parser.add_argument("-b", "--baud", default=115200, type=int, help="Baud rate")
    parser.add_argument("-i", "--interval", default=0.02, type=float, help="Fade-out interval for events")
    parser.add_argument("-f", "--fps", default=100, type=int, help="Dispaly frames per second")
    parser.add_argument("-s", "--scaleup", default=4, type=int, help="Scale-up factor")
    parser.add_argument("-m", "--movie", default=None, help="Movie file name")
    args = parser.parse_args()

    # Create a video file to save the movie if indicated
    out = cv2.VideoWriter(args.movie, cv2.VideoWriter_fourcc('M','J','P','G'), args.fps, (128*args.scaleup,128*args.scaleup)) \
            if args.movie is not None  else None

    # Track time so we can stop displaying old events
    counts = np.zeros((128,128)).astype('uint8')

    # Start with an empty image
    image = np.zeros((128,128,3)).astype('uint8')

    # Compute number of iterations before events should disappear, based on
    # 1msec display assumption
    ageout = int(args.interval * 1000)

    port = serial.Serial(args.port, args.baud)

    x, y, p = 0, 0, 0

    state = STATE_NONE

    while True:

        val = ord(port.read())

        if val == EOM:
            state = STATE_BEGIN

        elif state == STATE_BEGIN:
            state = STATE_GET_X

        elif state == STATE_GET_X:
            state = STATE_GET_Y

        elif state == STATE_GET_Y:
            state = STATE_GET_P

        elif state == STATE_GET_P:
            state = STATE_NONE

        if state == STATE_GET_X:
            x = val

        elif state == STATE_GET_Y:
            y = val

        elif state == STATE_GET_P:
            p = -1 if val == 255 else 1
            print(x, y, p)

    cv2.destroyAllWindows()

if __name__ == '__main__':

    main()

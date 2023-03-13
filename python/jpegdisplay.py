#!/usr/bin/python3
'''
Copyright (C) 2023 Simon D. Levy

Read and display JPEG-compressed event images over USB

MIT License
'''

import serial
import numpy as np
import cv2

SCALEUP = 2
DELAY_MSEC = 15


def main():

    # Connect to Teensy
    port = serial.Serial('/dev/ttyACM0', 115200, timeout=0.02)

    # count = 0

    try:

        while(True):

            image = np.zeros((128, 128))

            img_data = port.read(10_000)

            if len(img_data) > 0:

                jpg_as_np = np.frombuffer(img_data, dtype=np.uint8)

                image = cv2.imdecode(jpg_as_np, flags=cv2.IMREAD_GRAYSCALE)

                if image is not None:

                    bigimage = cv2.resize(image, (128*SCALEUP, 128*SCALEUP))

                    cv2.imshow('image', bigimage)

                    if cv2.waitKey(DELAY_MSEC) == 27:  # ESC
                        break

    except KeyboardInterrupt:

        port.close()


main()

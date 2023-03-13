#!/usr/bin/python3
'''
Copyright (C) 2023 Simon D. Levy

MIT License
'''

import serial
import numpy as np
import cv2

SCALEUP = 2

def main():

    # Connect to Teensy
    port = serial.Serial('/dev/ttyACM0', 115200, timeout=0.02);

    # count = 0

    try:

        while(True):

            image = np.zeros((128,128))

            img_data = port.read(10_000)

            if len(img_data) > 0:

                jpg_as_np = np.frombuffer(img_data, dtype=np.uint8)
                image = cv2.imdecode(jpg_as_np, flags=1)

                bigimage = cv2.resize(image, (128*SCALEUP,128*SCALEUP))

                cv2.imshow('image', bigimage)

                if cv2.waitKey(1) == 27:  # ESC
                    break

    except KeyboardInterrupt:

        port.close()

main()


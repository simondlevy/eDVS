#!/usr/bin/env python3

PORT = '/dev/ttyUSB0'

import serial
from time import time, sleep
import cv2
import numpy as np
from threading import Thread

def send(port, cmd):

    port.write((cmd + '\n').encode())
    sleep(.01)

def read_sensor(image, times, flags):

    port = serial.Serial(port=PORT, baudrate=12000000, rtscts=True)

    # Reset board
    send(port, 'R')

    # Enable event sending
    send(port, 'E+')

    # Use two-byte event format
    send(port, '!E0')

    x      = None
    second = False

    while flags[0]:

        v = ord(port.read()) & 0b01111111

        if second:
            y = v
            image[x,y] = 1.0
            times[x,y] = time()
        else:
            x = v

        second = not second

    print('done')

def main():

    image = np.zeros((128,128))

    times = np.zeros((128,128))

    flags = [True]

    thread = Thread(target=read_sensor, args = (image,times,flags))
    thread.daemon = True
    thread.start()

    while(True):

        # Zero out pixels with events older than a certain time before now
        image[(time() - times) > .10] = 0

        # Display the resulting image
        cv2.imshow('image', cv2.resize(image, ((512,512))))
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

    flags[0] = False

    thread.join()

if __name__ == '__main__':

    main()

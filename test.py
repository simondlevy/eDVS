#!/usr/bin/env python3

PORT = '/dev/ttyUSB0'

import serial
from time import sleep
import cv2
import numpy as np
from threading import Thread

def send(port, cmd):

    port.write((cmd + '\n').encode())
    sleep(.01)

def read_sensor():

    port = serial.Serial(port=PORT, baudrate=12000000, rtscts=True)

    # Reset board
    send(port, 'R')

    # Enable event sending
    send(port, 'E+')

    # Use two-byte event format
    send(port, '!E0')

    x      = None
    second = False

    while True:

        v = ord(port.read()) & 0b01111111

        if second:
            print(x, v)
        else:
            x = v

        second = not second

def main():

    #thread = Thread(target=read_sensor, args = (plotter,))
    thread = Thread(target=read_sensor)
    thread.daemon = True
    thread.start()

    while(True):

        image = np.zeros((128,128))

        # Display the resulting image
        cv2.imshow('image', cv2.resize(image, ((512,512))))
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':

    main()

#!/usr/bin/env python3

PORT = '/dev/ttyUSB0'

import serial
from time import sleep

def send(port, cmd):

    port.write((cmd + '\n').encode())
    sleep(.01)


def main():

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

if __name__ == '__main__':

    main()

#!/usr/bin/env python3

PORT = '/dev/ttyUSB0'

import serial
from time import sleep

def send(port, cmd):

    port.write((cmd + '\n').encode())
    sleep(.01)


def main():

    port = serial.Serial(port=PORT, baudrate=12000000, rtscts=True)

    send(port, 'R')

    send(port, 'E+')

    send(port, '!E0')

    while True:
        c = ord(port.read())
        print('%0X' % c)

if __name__ == '__main__':

    main()

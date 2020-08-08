#!/usr/bin/env python3

PORT = '/dev/ttyUSB0'

import serial

def send(port, cmd):

    port.write((cmd + '\n').encode())

def main():

    port = serial.Serial(port=PORT, baudrate=12000000, rtscts=True)

    send(port, 'R')

    send(port, 'E+')

    send(port, '!E0')

    while True:
        print(port.read())

if __name__ == '__main__':

    main()

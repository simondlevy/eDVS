#!/usr/bin/env python3

PORT = '/dev/ttyUSB0'

import serial

port = serial.Serial(port=PORT, baudrate=12000000, rtscts=True)

port.write('R\n'.encode())

port.write('E+\n'.encode())

port.write('!E0\n'.encode())

while True:
    print(port.read())


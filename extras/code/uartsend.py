#!/usr/bin/env python3

import serial

port = serial.Serial('/dev/ttyUSB1', 115200)

while True:

    try:

        port.write('A'.encode())

    except KeyboardInterrupt:

        break

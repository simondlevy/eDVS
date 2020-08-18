#!/usr/bin/env python3

import serial

port = serial.Serial('/dev/ttyUSB1', 115200)

c = 0

while True:

    try:

        port.write(chr(65+c).encode()) # 65 = 'A'

        c =  (c+1) % 26

    except KeyboardInterrupt:

        break

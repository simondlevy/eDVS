#!/usr/bin/env python3
'''
Test UART at maximum ESP32 Baud rate

Copyright (C) 2020 Simon D. Levy

MIT License
'''

PORT = '/dev/ttyUSB1'
BAUD = 4000000

import serial

port = serial.Serial(PORT, BAUD)

c = 0

while True:

    try:

        port.write(chr(65+c).encode()) # 65 = 'A'

        c =  (c+1) % 26

    except KeyboardInterrupt:

        break

#!/usr/bin/env python3
'''
Copyright (C) 2023 Simon D. Levy

MIT License
'''

import serial

def main():

    # Connect to Teensy
    port = serial.Serial('/dev/ttyACM0', 115200, timeout=0.02);

    count = 0

    try:

        while(True):

            buf = port.read(100_000_000)

            if len(buf) > 0:
                f = open('images/image%04d.jpg' % count, 'wb')
                print(len(buf))
                f.write(buf)
                f.close()
                count += 1

    except KeyboardInterrupt:

        port.close()

main()


#!/usr/bin/env python3
'''
Copyright (C) 2023 Simon D. Levy

MIT License
'''

import serial

def main():

    # Connect to Teensy
    port = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1);

    f = open('tmp.jpg', 'wb')

    try:

        while(True):

            buf = port.read(100_000_000)

            if len(buf) > 0:
                print(len(buf))
                f.write(buf)
                exit(0)

    except KeyboardInterrupt:

        port.close()

main()


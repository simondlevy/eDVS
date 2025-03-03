#!/usr/bin/python3
'''
Simple demo of the iniVation Mini eDVS via FTDI adapter

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from edvs import EDVS
import argparse
import traceback


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('-p', '--port', default='/dev/ttyUSB0',
                           help='Port (/dev/ttyUSB0, COM5, etc.')

    argparser.add_argument('-b', '--baud', default=2000000, type=int,
                           help='Baud rate')

    args = argparser.parse_args()

    # Connect to sensor
    edvs = EDVS(args.port, args.baud)

    try:
        print(edvs.version())

    # Stop streaming on error
    except Exception:
        traceback.print_exc()
        edvs.reset()
        exit(0)


if __name__ == '__main__':

    main()

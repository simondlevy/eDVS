#!/usr/bin/env python3

import numpy as np
import argparse
import serial
import cv2
from time import time


class TimerTask:

    def __init__(self):

        self.sec_prev = 0

    def ready(self, freq_hz):

        sec_curr = time()

        result = False

        if sec_curr - self.sec_prev > 1.0 / freq_hz:

            if self.sec_prev > 0:
                result = True

            self.sec_prev = sec_curr

        return result


def newFrameBuf():
    return np.array([], dtype=np.uint8)


def main():

    argparser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    argparser.add_argument('-p', '--port', default='/dev/ttyACM0',
                           help='Serial port')

    argparser.add_argument('-b', '--bufsize', default=2048, type=int,
                           help='Buffer size')

    argparser.add_argument('-s', '--scaleup', default=2, type=int,
                           help='Image scale-up')

    args = argparser.parse_args()

    reportTask = TimerTask()

    frameTask = TimerTask()

    # See https://www.pjrc.com/teensy/td_serial.html for why we don't specify
    # baud rate
    with serial.Serial(args.port) as port:

        try:

            bytes_per_second = 0

            frame_buf = newFrameBuf()

            while True:

                new_buf = np.frombuffer(port.read(args.bufsize),
                                        dtype=np.uint8)

                frame_buf = np.append(frame_buf, new_buf)

                n = len(new_buf)

                bytes_per_second += n

                if frameTask.ready(30):

                    image = np.zeros((128, 128), dtype=np.uint8)

                    x = frame_buf[0::2]
                    y = frame_buf[1::2]

                    try:

                        image[x, y] = 255

                        bigimage = cv2.resize(image,
                                              (128*args.scaleup, 128*args.scaleup))

                        cv2.imshow('Teensy on %s' % args.port, bigimage)

                        if cv2.waitKey(1) == 27:
                            break

                    # XXX need to figure out why this is happening
                    except IndexError as e:

                        print(e)

                    frame_buf = newFrameBuf()

                if reportTask.ready(1):
                    print('%d events / second' % (bytes_per_second//2))
                    bytes_per_second = 0

        except KeyboardInterrupt:
            exit(0)


main()

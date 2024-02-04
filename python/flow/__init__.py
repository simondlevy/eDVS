'''
DVS utilities

Copyright (C) 2023 Simon D. Levy

MIT License
'''

import numpy as np
import cv2
from time import time

try:
    from dvs_filters.stcf import SpatioTemporalCorrelationFilter
    from dvs_filters.knoise import Knoise
    from dvs_filters.passthru import PassThruFilter

except:
    print('Please install https://github.com/simondlevy/dvs-filters')
    exit(0)


def parse_args(argparser):

    argparser.add_argument('-f', '--fps', type=int, default=30,
                           help='Frame rate per second for display')

    argparser.add_argument('-c', '--color', action='store_true',
                           help='Display in color')

    argparser.add_argument('-d', '--denoising', default='none',
                           choices=('stcf', 'knoise', 'none'),
                           help='Denoising filter choice')

    argparser.add_argument('-t', '--maxtime', type=float,
                           help='Maximum time to play in seconds')

    argparser.add_argument('-v', '--video', default=None,
                           help='Name of video file to save')

    argparser.add_argument('-s', '--scaleup', type=int, default=2,
                           help='Scale-up factor for display')

    args = argparser.parse_args()

    return args


class FlowDisplay:

    # Not sure why we need this, but without it video output is slower
    VIDEO_FPS_SCALE = 5

    def __init__(self, name, args):

        # For display window
        self.name = name

        self.scaleup = args.scaleup
        self.fps = args.fps
        self.maxtime = args.maxtime
        self.color = args.color

        # Start with empty images
        self.clear()

        # Helps group events into frames
        self.frames_this_second = 0

        # Supports statistics reporting
        self.raw_total = 0
        self.flt_total = 0
        self.raw_per_second = 0
        self.flt_per_second = 0

        self.denoise = (Knoise()
                        if args.denoising == 'knoise'
                        else SpatioTemporalCorrelationFilter()
                        if args.denoising == 'stcf'
                        else PassThruFilter())

        self.video_out = (self._video_writer(args)
                          if args.video is not None else None)

        # Supports quitting after a specified time
        self.time_start = time()

        self.total_denoise_time = 0
        self.total_event_count = 0

    def addEvent(self, e):
        '''
        Returns True if event passed denoising filter, False otherwise
        '''

        passed = False

        # Add event to raw image
        self.raw_image[e.y, e.x] = self._polarity2color(e)
        self.raw_total += 1

        # Add event to filtered image if event passes the filter
        beg = time()
        passed = self.denoise.check(e)
        self.total_denoise_time += (time() - beg)
        if passed:
            self.flt_image[e.y, e.x] = self._polarity2color(e)
            self.flt_total += 1
            passed = True

        self.total_event_count += 1

        return passed

    def show(self):
        '''
        Returns False on quit, True otherwise
        '''

        #if (self.total_event_count > 1):
        #    print('%3.3e' % (self.total_denoise_time / self.total_event_count))

        big_image = np.hstack((self._enlarge(self.raw_image, self.scaleup),
                               self._enlarge(self.flt_image, self.scaleup),
                               self._enlarge(self.flt_image, self.scaleup),
                               ))

        # Draw a line down the middle of the big image to separate
        # raw from filtered
        big_image[:, 128*self.scaleup] = 255

        self._add_events_per_second(big_image, 50, self.raw_per_second)
        self._add_events_per_second(big_image, 300, self.flt_per_second)

        # Show big image, quitting on ESC
        cv2.imshow(self.name, big_image)
        if cv2.waitKey(1) == 27:
            return False

        # Save current big image frame if indicated
        if self.video_out is not None:
            self.video_out.write(big_image)

        # Update events-per-second totals every second
        self.frames_this_second += 1
        if self.frames_this_second == self.fps:

            # Update stats for reporting
            self.raw_per_second = self.raw_total
            self.flt_per_second = self.flt_total
            self.raw_total = 0
            self.flt_total = 0
            self.frames_this_second = 0

        # Quit after specified time if indicated
        if (self.maxtime is not None and
                time() - self.time_start >= self.maxtime):
            return False

        return True

    def close(self):

        cv2.destroyAllWindows()

        if self.video_out is not None:
            self.video_out.release()

    def clear(self):

        self.raw_image = self._new_image()
        self.flt_image = self._new_image()

    def _video_writer(self, args):

        return (cv2.VideoWriter(args.video,
                                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                self.VIDEO_FPS_SCALE * self.fps,
                                (self.scaleup * 384, self.scaleup * 128)))

    def _new_image(self):

        return np.zeros((128, 128, 3), dtype=np.uint8)

    def _enlarge(self, image, factor):

        return cv2.resize(image, (128*factor, 128*factor))

    def _polarity2color(self, e):

        return (((0, 255, 0) if e.polarity else (0, 0, 255))
                if self.color else (255, 255, 255))

    def _add_events_per_second(self, image, xpos, value):

        if value > 0:

            cv2.putText(image,
                        '%d events/second' % value,
                        (xpos, 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,            # scale
                        (0, 255, 255),  # color
                        2,              # thickness
                        2)              # line type

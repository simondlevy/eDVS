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

    argparser.add_argument('-r', '--rate', type=int, default=30,
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

    argparser.add_argument('-f', '--flowtiles', type=int, default=1, # XXX stick to 2x2 for now
                           help='n in 2^n x 2^n tiles for optical flow')

    args = argparser.parse_args()

    return args


class Display:

    # Not sure why we need this, but without it video output is slower
    VIDEO_FPS_SCALE = 5

    def __init__(self, name, args):

        # For display window
        self.name = name

        self.scaleup = args.scaleup
        self.fps = args.rate
        self.maxtime = args.maxtime
        self.color = args.color
        self.flowtiles = 2 ** args.flowtiles
        self.tilesize = 128 // self.flowtiles

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
        if passed and e.x < 64 and e.y < 64: # XXX stick to upper-left quadrant for now
            tile_col = e.x // self.tilesize
            tile_row = e.y // self.tilesize
            self.x_sum_per_tile[tile_row][tile_col] += e.x
            self.y_sum_per_tile[tile_row][tile_col] += e.y
            self.count_per_tile[tile_row][tile_col] += 1
            self.flt_image[e.y, e.x] = self._polarity2color(e)
            self.flt_total += 1
            passed = True

        self.total_event_count += 1

        return passed

    def show(self):
        '''
        Returns False on quit, True otherwise
        '''

        count = self.count_per_tile[0][0]

        if count > 0:

            ctrx = int(self.x_sum_per_tile[0][0] / count)
            ctry = int(self.y_sum_per_tile[0][0] / count)

            self.flo_image[ctry][ctrx] = (255, 255, 255)

        #if (self.total_event_count > 1):
        #    print('%3.3e' % (self.total_denoise_time / self.total_event_count))

        big_image = np.hstack((self._enlarge(self.raw_image, self.scaleup),
                               self._enlarge(self.flt_image, self.scaleup),
                               self._enlarge(self.flo_image, self.scaleup),
                               ))

        # Draw lines down the middle of the big image to separate
        # panels
        self._draw_line(big_image, 1)
        self._draw_line(big_image, 2)

        # Add panel titles
        self._add_events_per_second(big_image, 50, self.raw_per_second)
        self._add_events_per_second(big_image, 300, self.flt_per_second)
        self._add_title(big_image, 620, 'Flow')

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
        self.flo_image = self._new_image()

        self.x_sum_per_tile = np.zeros((self.flowtiles, self.flowtiles))
        self.y_sum_per_tile = np.zeros((self.flowtiles, self.flowtiles))
        self.count_per_tile = np.zeros((self.flowtiles, self.flowtiles))

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

            self._add_title(image, xpos, '%d events/second' % value)

    def _add_title(self, image, xpos, title):

        cv2.putText(image,
                    title,
                    (xpos, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,            # scale
                    (0, 255, 255),  # color
                    1,              # thickness
                    2)              # line type
        

    def _draw_line(self, big_image, k):

        big_image[:, k * 128 * self.scaleup] = 255


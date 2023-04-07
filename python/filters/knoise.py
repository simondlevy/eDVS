'''
DVS event filtersing

Adapted from Java code in
  https:#github.com/SensorsINI/jaer/tree/master/src/net/sf/jaer/eventprocessing/filter

Copyright (C) 2023 Simon D. Levy

MIT License
'''

import numpy as np


class OrderNbackgroundActivityFilter:

    DEFAULT_TIMESTAMP = 0

    def __init__(self, last_timestamp, sx=128, sy=128, dt_msec=10, supporters=10):

        self.sx = sx
        self.sy = sy

        self.dt_usec = 1000 * dt_msec
        self.supporters = supporters

        self.last_row_ts = self.DEFAULT_TIMESTAMP * np.ones(sy)
        self.last_col_ts = self.DEFAULT_TIMESTAMP * np.ones(sx)

        self.last_x_by_row = np.zeros(sx)
        self.last_y_by_col = np.zeros(sy)

        self.initialize_last_times_map_for_noise_rate(last_timestamp)

    def check(self, e):
        '''
        Returns True if event e passes filter, False otherwise
        '''

        # assume all edge events are noise and filter out
        if (e.x <= 0 or e.y <= 0
            or e.x >= self.sx - self.supporters or e.y >= self.sy - self.supporters):
            return False

        # first check rows around us, if any adjancent row has event then
        # filter in
        for y in range(-self.supporters, self.supporters+1):
            if (self.last_row_ts[e.y + y] != self.DEFAULT_TIMESTAMP
                and e.timestamp - self.last_row_ts[e.y + y] < self.dt_usec
                and abs(self.last_x_by_row[e.y + y] - e.x) <= 1):
                # if there was event (ts!=DEFAULT_TIMESTAMP), and the timestamp
                # is recent enough, and the column was adjacent, then filter in
                self._save_event(e)
                return True

        # now do same for columns
        for x in range(-self.supporters, self.supporters+1):
            if (self.last_col_ts[e.x + x] != self.DEFAULT_TIMESTAMP
                and e.timestamp - self.last_col_ts[e.x + x] < self.dt_usec
                and abs(self.last_y_by_col[e.x + x] - e.y) <= 1):
                self._save_event(e)
                return True

        return False

    def _save_event(self, e):
        self.last_x_by_row[e.y] = e.x
        self.last_y_by_col[e.x] = e.y
        self.last_col_ts[e.x] = e.timestamp
        self.last_row_ts[e.y] = e.timestamp

    def initialize_last_times_map_for_noise_rate(self,
                                                 last_timestamp_us,
                                                 noise_rate_hz=.1):
        ''''
        Fills 1d arrays with random events with waiting times drawn from
        Poisson process with rate noise_rate_hz

        @param noise_rate_hz rate in Hz

        @param last_timestamp_us the last timestamp; waiting times are created
        before this time
        '''

        for i in range(len(self.last_row_ts)):
            p = np.random.random()
            t = -noise_rate_hz * np.log(1 - p)
            tUs = int((1000000 * t))
            self.last_row_ts[i] = last_timestamp_us - tUs
            self.last_x_by_row[i] = np.random.randint(self.sy)

        for i in range(len(self.last_col_ts)):
            p = np.random.random()
            t = -noise_rate_hz * np.log(1 - p)
            tUs = int(1000000 * t)
            self.last_col_ts[i] = last_timestamp_us - tUs
            self.last_y_by_col[i] = np.random.randint(self.sx)

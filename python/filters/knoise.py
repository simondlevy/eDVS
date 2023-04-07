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

    def __init__(self, sx=128, sy=128, delta_t_msec=1, supporters=1):

        self.sx = sx
        self.sy = sy

        self.delta_t_usec = 1000 * delta_t_msec
        self.supporters = supporters

        self.last_row_ts = self.DEFAULT_TIMESTAMP * np.ones(sy)
        self.last_col_ts = self.DEFAULT_TIMESTAMP * np.ones(sx)

        self.last_x_by_row = np.zeros(sx)
        self.last_y_by_col = np.zeros(sy)

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
               return True

        # now do same for columns
        for x in range(-self.supporters, self.supporters+1):
            if (self.last_col_ts[e.x + x] != self.DEFAULT_TIMESTAMP
                and e.timestamp - self.last_col_ts[e.x + x] < self.dt_usec
                and abs(self.last_y_by_col[e.x + x] - e.y) <= 1):
                return True

        return False

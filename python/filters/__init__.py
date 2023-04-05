'''
DVS event filtersing

Adapted from Java code in
  https:#github.com/SensorsINI/jaer/tree/master/src/net/sf/jaer/eventprocessing/filter

Copyright (C) 2023 Simon D. Levy

MIT License
'''

import numpy as np

class _NnbRange:

    def __init__(self):

        self.x0 = 0
        self.x1 = 0
        self.y0 = 0
        self.y1 = 0

    def compute(self, x,  y,  ssx,  ssy, sigma_dist_pixels):

        d = sigma_dist_pixels

        self.x0 = 0 if x < d else x - d
        self.y0 = 0 if y < d else y - d
        self.x1 = ssx - d if x >= (ssx - d) else x + d
        self.y1 = ssy - d if y >= (ssy - d) else y + d


class SpatioTemporalCorrelationFilter:

    DEFAULT_TIMESTAMP = 0

    def __init__(
            self, 
            size_x=128,
            size_y=128,
            filter_hot_pixels=True,
            subsample_by=1,
            sigma_dist_pixels=1,
            let_first_event_through=True):

        self.sxm1 = size_x - 1
        self.sym1 = size_y - 1

        self.ssx = self.sxm1 >> subsample_by
        self.ssy = self.sym1 >> subsample_by

        self.fhp = filter_hot_pixels
        self.subsample_by = subsample_by
        self.let_first_event_through = let_first_event_through
        self.sigma_dist_pixels = sigma_dist_pixels

        self.total_event_count = 0

        self.timestamp_image = np.zeros((128,128))

    def step(self, e):

        self.total_event_count += 1

        ts = e.timestamp

        # subsampling address
        x = e.x >> self.subsample_by
        y = e.y >> self.subsample_by

        # special handling for first event
        if self.timestamp_image[x][y] == self.DEFAULT_TIMESTAMP:
            self.timestamp_image[x][y] = ts
            if self.total_event_count == 1:
                return self.let_first_event_through

        # the real denoising starts here

        ncorrelated = 0
       
        nnb_range = _NnbRange()
        nnb_range.compute(x, y, self.ssx, self.ssy, self.sigma_dist_pixels)
        

        breakouter = False

        for xx in range(nnb_range.x0, nnb_range.x1 + 1):

            if breakouter:
                break

            col = self.timestamp_image[xx]

            for yy in range(nnb_range.y0, nnb_range.y1 + 1):

                if self.fhp and xx == x and yy == y:
                    continue # like BAF, don't correlate with ourself

                last_t = col[yy]

                # deltaT will be very negative for DEFAULT_TIMESTAMP because of overflow
                deltaT = ts - last_t
'''
        outerloop:
        for (int xx = nnbRange.x0 xx <= nnbRange.x1 xx++) {
             int[] col = self.timestamp_image[xx]
            for (int yy = nnbRange.y0 yy <= nnbRange.y1 yy++) {
                if (fhp && xx == x && yy == y) {
                    continue # like BAF, don't correlate with ourself
                }
                 int last_t = col[yy]
                 int deltaT = (ts - last_t) # note deltaT will be very negative for DEFAULT_TIMESTAMP because of overflow

                if (deltaT < dt && last_t != DEFAULT_TIMESTAMP) { # ignore correlations for DEFAULT_TIMESTAMP that are neighbors which never got event so far
                    ncorrelated++
                    if (ncorrelated >= numMustBeCorrelated) {
                        break outerloop # csn stop checking now
                    }
                }
            }
        }
        if (ncorrelated < numMustBeCorrelated) {
            filterOut(e)
        } else {
            filterIn(e)
        }
'''

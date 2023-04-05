'''
DVS event filtersing

Adapted from Java code in
  https:#github.com/SensorsINI/jaer/tree/master/src/net/sf/jaer/eventprocessing/filter

Copyright (C) 2023 Simon D. Levy

MIT License
'''

import numpy as np

class SpatioTemporalCorrelationFilter:

    DEFAULT_TIMESTAMP = 0

    def __init__(self, subsample_by=1, let_first_event_through=True):

        self.subsample_by = subsample_by

        self.let_first_event_through = let_first_event_through

        self.total_event_count = 0

        self.timestamp_image = np.zeros((128,128))

    def step(self, e):

        self.total_event_count += 1

        ts = e.timestamp

        # subsampling address
        x = e.x >> self.subsample_by
        y = e.y >> self.subsample_by

        if self.timestamp_image[x][y] == self.DEFAULT_TIMESTAMP:

            self.timestamp_image[x][y] = ts

            if self.total_event_count == 1:

                return self.let_first_event_through


'''
    if (self.timestamp_image[x][y] == DEFAULT_TIMESTAMP) {
        self.timestamp_image[x][y] = ts;
        if (letFirstEventThrough) {
            filterIn(e);
            continue;
        } else {
            filterOut(e);
            continue;
        }
    }

    # finally the real denoising starts here
    int ncorrelated = 0;
    nnbRange.compute(x, y, ssx, ssy);
    outerloop:
    for (int xx = nnbRange.x0; xx <= nnbRange.x1; xx++) {
        final int[] col = self.timestamp_image[xx];
        for (int yy = nnbRange.y0; yy <= nnbRange.y1; yy++) {
            if (fhp && xx == x && yy == y) {
                continue; # like BAF, don't correlate with ourself
            }
            final int lastT = col[yy];
            final int deltaT = (ts - lastT); # note deltaT will be very negative for DEFAULT_TIMESTAMP because of overflow

            if (deltaT < dt && lastT != DEFAULT_TIMESTAMP) { # ignore correlations for DEFAULT_TIMESTAMP that are neighbors which never got event so far
                ncorrelated++;
                if (ncorrelated >= numMustBeCorrelated) {
                    break outerloop; # csn stop checking now
                }
            }
        }
    }
    if (ncorrelated < numMustBeCorrelated) {
        filterOut(e);
    } else {
        filterIn(e);
    }
'''

'''
DVS event filtersing

Adapted from Java code in
  https://github.com/SensorsINI/jaer/tree/master/src/net/sf/jaer/eventprocessing/filter

Copyright (C) 2023 Simon D. Levy

MIT License
'''

import numpy as np

class SpatioTemporalCorrelationFilter:

    def __init__(self):

        pass


'''
    totalEventCount++;
    int ts = e.timestamp;
    final int x = (e.x >> subsampleBy), y = (e.y >> subsampleBy); // subsampling address
    if ((x < 0) || (x > ssx) || (y < 0) || (y > ssy)) { // out of bounds, discard (maybe bad USB or something)
        filterOut(e);
        continue;
    }
    if (timestampImage[x][y] == DEFAULT_TIMESTAMP) {
        timestampImage[x][y] = ts;
        if (letFirstEventThrough) {
            filterIn(e);
            continue;
        } else {
            filterOut(e);
            continue;
        }
    }

    // finally the real denoising starts here
    int ncorrelated = 0;
    nnbRange.compute(x, y, ssx, ssy);
    outerloop:
    for (int xx = nnbRange.x0; xx <= nnbRange.x1; xx++) {
        final int[] col = timestampImage[xx];
        for (int yy = nnbRange.y0; yy <= nnbRange.y1; yy++) {
            if (fhp && xx == x && yy == y) {
                continue; // like BAF, don't correlate with ourself
            }
            final int lastT = col[yy];
            final int deltaT = (ts - lastT); // note deltaT will be very negative for DEFAULT_TIMESTAMP because of overflow

            if (deltaT < dt && lastT != DEFAULT_TIMESTAMP) { // ignore correlations for DEFAULT_TIMESTAMP that are neighbors which never got event so far
                ncorrelated++;
                if (ncorrelated >= numMustBeCorrelated) {
                    break outerloop; // csn stop checking now
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

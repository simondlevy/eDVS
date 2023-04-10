/*
DVS Knoise event filtering. Runs filter in O(N), N = sensor resolution.

Adapted from Java code in
https:#github.com/SensorsINI/jaer/tree/master/src/net/sf/jaer/eventprocessing/filter


Copyright (C) 2023 Simon D. Levy

MIT License
 */

#include <limits.h>

#include "edvs.h"

class OrderNbackgroundActivityFilter {

    public:

        OrderNbackgroundActivityFilter(
                const uint32_t last_timestamp=4294967295,
                const uint8_t sx=128, 
                const uint8_t sy=128, 
                const uint32_t dt_msec=10,
                const uint8_t supporters=10)
        {
            (void)last_timestamp;
            (void)sx;
            (void)sy;
            (void)dt_msec;
            (void)supporters;
        }

        bool check(const EDVS::event_t & e)
        {
            return true;
        }
};

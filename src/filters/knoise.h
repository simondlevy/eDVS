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
            _sx = sx;
            _sy = sy;
            _supporters = supporters;

            _dt_usec = 1000 * dt_msec;

            for (uint8_t k=0; k<128; ++k) {
                _last_row_ts[k] = DEFAULT_TIMESTAMP;
                _last_col_ts[k] = DEFAULT_TIMESTAMP;
                _last_x_by_row[k] = 0;
                _last_y_by_col[k] = 0;
            }
        }

        bool check(const EDVS::event_t & e)
        {
            return true;
        }

    private:

        static const uint32_t DEFAULT_TIMESTAMP = 0;

        uint8_t _sx;
        uint8_t _sy;
        uint32_t _dt_usec;
        uint8_t _supporters;

        uint32_t _last_row_ts[128];
        uint32_t _last_col_ts[128];

        uint8_t _last_x_by_row[128];
        uint8_t _last_y_by_col[128];

 };

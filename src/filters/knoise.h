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
                const uint32_t dt_msec=100,
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

            initialize_last_times_map_for_noise_rate(last_timestamp);
        }

        bool check(const EDVS::event_t & e)
        {
            // assume all edge events are noise and filter out
            if (e.x <= 0 || e.y <= 0 ||
                    e.x >= _sx - _supporters || e.y >= _sy - _supporters) {

                return false;
            }

            return 
                check_row_or_col(e, _last_row_ts, _last_x_by_row, e.y, e.x) ||
                check_row_or_col(e, _last_col_ts, _last_y_by_col, e.x, e.y);
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

        void initialize_last_times_map_for_noise_rate(
                const uint32_t last_timestamp_us,
                const float noise_rate_hz = 0.1)
        {
            /*
               Fills 1d arrays with random events with waiting times drawn from
               Poisson process with rate noise_rate_hz

               @param noise_rate_hz rate in Hz

               @param last_timestamp_us the last timestamp; waiting times are created
               before this time
             */

            initialize_row_or_col(_last_row_ts, _last_x_by_row, _sx, 
                    noise_rate_hz, last_timestamp_us);

            initialize_row_or_col(_last_col_ts, _last_y_by_col, _sy, 
                    noise_rate_hz, last_timestamp_us);
        }

        void initialize_row_or_col(
                uint32_t ts[],
                uint8_t x_or_y[], 
                const uint8_t s, 
                const float noise_rate_hz, 
                const uint32_t last_timestamp_us)
        {
            for (uint8_t i=0; i<128; ++i) {

                const float p = (float)random() / LONG_MAX;
                const float t = -noise_rate_hz * log(1 - p);
                const uint32_t tUs = (int)(1000000 * t);

                ts[i] = last_timestamp_us - tUs;
                x_or_y[i] = random(s);
            }
        }

        bool check_row_or_col(
                const EDVS::event_t & e,
                const uint32_t ts[], 
                const uint8_t x_or_y[], 
                const uint8_t coord, 
                const uint8_t other)
        {
            for (int8_t k=-_supporters; k<=_supporters; ++k) {

                Serial.printf("e.t=%u  ts[coord+k]=%u  dt_usec%u  <=%d\n",
                        (unsigned)e.t,
                        (unsigned)ts[coord + k],
                        (unsigned)_dt_usec,
                        e.t - ts[coord + k] < _dt_usec);

                if (
                        // if there was event (ts!=DEFAULT_TIMESTAMP), and the timestamp
                        // is recent enough, and the column was adjacent, then filter in
                        ts[coord + k] != DEFAULT_TIMESTAMP &&
                        e.t - ts[coord + k] < _dt_usec &&
                        abs(x_or_y[coord + k] - other) <= 1) {

                    save_event(e);
                    return true;
                }
            }

            return false;
        }

        void save_event(const EDVS::event_t & e)
        {
            _last_x_by_row[e.y] = e.x;
            _last_y_by_col[e.x] = e.y;
            _last_col_ts[e.x] = e.t;
            _last_row_ts[e.y] = e.t;
        }
};

/*
DVS Knoise event filtering. Runs filter in O(N), N = sensor resolution.

Adapted from Java code in
  https:#github.com/SensorsINI/jaer/tree/master/src/net/sf/jaer/eventprocessing/filter


Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"

class OrderNbackgroundActivityFilter {

    private:

    public:

        OrderNbackgroundActivityFilter(
                uint32_t last_timestamp=4294967295,
                uint8_t sx=128, 
                uint8_t sy=128, 
                uint32_t dt_msec=10,
                uint8_t supporters=10)
        {
        }

};

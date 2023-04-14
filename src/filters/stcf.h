/*
   Spatio-Temporal Correlation Filter

   Copyright (C) 2023 Simon D. Levy

   MIT License
 */

#include "edvs.h"

class SpatioTemporalCorrelationFilter {

    public:

        SpatioTemporalCorrelationFilter(uint8_t subsampleBy=0)
        {
            _subsampleBy = subsampleBy;

            _ssx = SXM1 >> _subsampleBy;
            _ssy = SYM1 >> _subsampleBy;
        }

        bool check(const EDVS::event_t & e)
        {
            const auto ts = e.t;

            const auto x = e.x >> _subsampleBy;
            const auto y = e.y >> _subsampleBy;

            // out of bounds, discard
            if (x < 0 || x > _ssx || y < 0 || y > _ssy) { 
                return false;
            }

            (void)ts;

            return true;
        }

    private:

        static const uint8_t SXM1 = 127;
        static const uint8_t SYM1 = 127;

        uint8_t _subsampleBy;

        uint8_t _ssx;
        uint8_t _ssy;
};

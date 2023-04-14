/*
   Spatio-Temporal Correlation Filter

   Copyright (C) 2023 Simon D. Levy

   MIT License
 */

#pragma once

#include "edvs.h"
#include "filter.h"

class SpatioTemporalCorrelationFilter : public AbstractNoiseFilter {

    public:

        SpatioTemporalCorrelationFilter(uint8_t subsampleBy=0)
        {
            _subsampleBy = subsampleBy;

            _ssx = SXM1 >> _subsampleBy;
            _ssy = SYM1 >> _subsampleBy;
        }

        virtual bool check(const EDVS::event_t & e) override
        {
            const auto ts = e.t;

            const auto x = e.x >> _subsampleBy;
            const auto y = e.y >> _subsampleBy;

            // out of bounds, discard
            if (x < 0 || x > _ssx || y < 0 || y > _ssy) { 
                return false;
            }

            (void)ts;

            /*
            if (timestampImage[x][y] == DEFAULT_TIMESTAMP) {
                storeTimestampPolarity(x, y, e);
                if (letFirstEventThrough) {
                    filterIn(e);
                    continue;
                } else {
                    filterOut(e);
                    continue;
                }
            }*/

            return true;
        }

    private:

        static const uint8_t SXM1 = 127;
        static const uint8_t SYM1 = 127;

        uint8_t _subsampleBy;

        uint8_t _ssx;
        uint8_t _ssy;
};

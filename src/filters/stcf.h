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

        SpatioTemporalCorrelationFilter(
                uint8_t subsampleBy=0,
                bool letFirstEventThrough=true
                )
        {
            _subsampleBy = subsampleBy;
            _letFirstEventThrough = letFirstEventThrough;

            _ssx = SXM1 >> _subsampleBy;
            _ssy = SYM1 >> _subsampleBy;

            for (uint8_t j=0; j<128; ++j) {
                for (uint8_t k=0; k<128; ++k) {
                    _timestampImage[j][k] = DEFAULT_TIMESTAMP;
                }
            }
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

            if (_timestampImage[x][y] == DEFAULT_TIMESTAMP) {

                storeTimestampPolarity(x, y, e);

                return _letFirstEventThrough;
            }

            // the real denoising starts here
            uint32_t ncorrelated = 0;

            (void)ncorrelated;

            /*
            nnbRange.compute(x, y, ssx, ssy);
            outerloop:
            for (int xx = nnbRange.x0; xx <= nnbRange.x1; xx++) {
                final int[] col = timestampImage[xx];
                for (int yy = nnbRange.y0; yy <= nnbRange.y1; yy++) {
                    if (fhp && xx == x && yy == y) {
                        continue; // like BAF, don't correlate with ourself
                    }
                    final int lastT = col[yy];
                    // note deltaT will be very negative for DEFAULT_TIMESTAMP
                    // because of overflow
                    final int deltaT = (ts - lastT); 
                    // ignore correlations for DEFAULT_TIMESTAMP that are
                    // neighbors which never got event so far
                    if (deltaT < dt && lastT != DEFAULT_TIMESTAMP) { 
                        ncorrelated++;
                        if (ncorrelated >= numMustBeCorrelated) {
                            break outerloop; // csn stop checking now
                        }
                    }
                }
            }*/

            bool filterIn = false;

            /*
            if (ncorrelated < numMustBeCorrelated) {
            } else {
                if (testFilterOutShotNoiseOppositePolarity(x, y, e)) {
                } else {
                    filterIn = true;
                }
            }*/

            storeTimestampPolarity(x, y, e);

            return filterIn;
        }

    private:

        static const uint8_t SXM1 = 127;
        static const uint8_t SYM1 = 127;

        uint8_t _subsampleBy;

        uint8_t _ssx;
        uint8_t _ssy;

        bool _letFirstEventThrough;

        uint8_t _timestampImage[128][1128];

        void storeTimestampPolarity(const uint8_t x, const uint8_t y, const EDVS::event_t e) 
        {
            _timestampImage[x][y] = e.t;

            //if (e instanceof PolarityEvent) {
            //    polImage[x][y] = (byte) ((PolarityEvent) e).getPolaritySignum();
            //}
        }
};

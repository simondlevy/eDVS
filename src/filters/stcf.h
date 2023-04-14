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
                bool letFirstEventThrough=true,
                bool filterHotPixels=false,
                float correlationTimeS=25e-3
                )
        {
            _subsampleBy = subsampleBy;
            _letFirstEventThrough = letFirstEventThrough;
            _filterHotPixels = filterHotPixels;

            _ssx = SXM1 >> _subsampleBy;
            _ssy = SYM1 >> _subsampleBy;

            for (uint8_t j=0; j<128; ++j) {
                for (uint8_t k=0; k<128; ++k) {
                    _timestampImage[j][k] = DEFAULT_TIMESTAMP;
                }
            }

            _dt = correlationTimeS * 1000000;

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

            nnbRange.compute(x, y, _ssx, _ssy);

            bool breakOuterLoop = false;

            for (uint8_t xx = nnbRange.x0; xx <= nnbRange.x1; xx++) {

                if (breakOuterLoop) {
                    break;
                }

                const uint8_t * col = _timestampImage[xx];

                for (uint8_t yy = nnbRange.y0; yy <= nnbRange.y1; yy++) {

                    if (_filterHotPixels && xx == x && yy == y) {
                        continue; // don't correlate with ourself
                    }

                    const auto lastT = col[yy];

                    // note deltaT will be very negative for DEFAULT_TIMESTAMP
                    // because of overflow
                    const auto deltaT = ts - lastT; 

                    // ignore correlations for DEFAULT_TIMESTAMP that are
                    // neighbors which never got event so far
                    if (deltaT < _dt && lastT != DEFAULT_TIMESTAMP) { 
                        ncorrelated++;
                        //if (ncorrelated >= numMustBeCorrelated) {
                        //    break outerloop; // csn stop checking now
                        //}
                    }
                }
            }

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

        uint32_t _dt;

        bool _letFirstEventThrough;
        bool _filterHotPixels;

        uint8_t _timestampImage[128][1128];

        NnbRange nnbRange;

        void storeTimestampPolarity(const uint8_t x, const uint8_t y, const EDVS::event_t e) 
        {
            _timestampImage[x][y] = e.t;

            //if (e instanceof PolarityEvent) {
            //    polImage[x][y] = (byte) ((PolarityEvent) e).getPolaritySignum();
            //}
        }
};

/*
   Spatio-Temporal Correlation Filter

   Adapted from 

   https://github.com/SensorsINI/jaer/blob/master/src/net/sf/jaer/eventprocessing/filter/
     SpatioTemporalCorrelationFilter.java

   Copyright (C) 2023 Simon D. Levy

   MIT License
 */

#pragma once

#include "edvs.hpp"
#include "filter.hpp"

class SpatioTemporalCorrelationFilter : public AbstractNoiseFilter {

    public:

        SpatioTemporalCorrelationFilter(
                uint8_t subsampleBy=0,
                bool letFirstEventThrough=true,
                bool filterHotPixels=false,
                float correlationTimeS=2.5e-2,
                uint8_t numMustBeCorrelated=2
                )
        {
            _subsampleBy = subsampleBy;
            _letFirstEventThrough = letFirstEventThrough;
            _filterHotPixels = filterHotPixels;
            _numMustBeCorrelated = numMustBeCorrelated;

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

            if (_timestampImage[x][y] == DEFAULT_TIMESTAMP) {

                storeTimestampPolarity(x, y, e);

                return _letFirstEventThrough;
            }

            // the real denoising starts here

            uint32_t ncorrelated = 0;

            nnbRange.compute(x, y, _ssx, _ssy);

            bool breakOuterLoop = false;

            for (uint8_t xx = nnbRange.x0; xx <= nnbRange.x1; xx++) {

                if (breakOuterLoop) {
                    break;
                }

                const auto col = _timestampImage[xx];

                for (uint8_t yy = nnbRange.y0; yy <= nnbRange.y1; yy++) {

                    if (_filterHotPixels && xx == x && yy == y) {
                        continue; // don't correlate with ourself
                    }

                    const auto lastT = col[yy];

                    // note deltaT will be very negative for DEFAULT_TIMESTAMP
                    // because of overflow
                    const auto deltaT = ts - lastT; 

                    // Serial.printf("(%d = %d - %d) < %d\n", deltaT, ts, lastT, _dt);

                    // ignore correlations for DEFAULT_TIMESTAMP that are
                    // neighbors which never got event so far
                    if (deltaT < _dt && lastT != DEFAULT_TIMESTAMP) { 
                        ncorrelated++;
                        if (ncorrelated >= _numMustBeCorrelated) {
                            breakOuterLoop = true; // csn stop checking now
                            break;
                        }
                    }
                }
            }

            bool filterIn = ncorrelated >= _numMustBeCorrelated /*&&
                !testFilterOutShotNoiseOppositePolarity(x, y, e)*/;

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

        uint8_t _numMustBeCorrelated;

        bool _letFirstEventThrough;
        bool _filterHotPixels;

        uint32_t _timestampImage[128][128];

        NnbRange nnbRange;

        void storeTimestampPolarity(
                const uint8_t x, const uint8_t y, const EDVS::event_t e) 
        {
            _timestampImage[x][y] = e.t;

            //if (e instanceof PolarityEvent) {
            //    polImage[x][y] = (byte) ((PolarityEvent) e).getPolaritySignum();
            //}
        }

        /**
         * Tests if event is perhaps a shot noise event that is very recently after
         * a previous event from this pixel and is the opposite polarity.
         *
         * @param x x address of event
         * @param y y address of event
         * @param e event
         *
         * @return true if noise event, false if signal
         */
        bool testFilterOutShotNoiseOppositePolarity(
                const uint8_t x, const uint8_t y, EDVS::event_t e) 
        {
            return false;

            /*
               if (!filterAlternativePolarityShotNoiseEnabled) {
               return false;
               }
               if (!(e instanceof PolarityEvent)) {
               return false;
               }
               numShotNoiseTests++;
               PolarityEvent p = (PolarityEvent) e;
               if (p.getPolaritySignum() == polImage[x][y]) {
               return false; // if same polarity, don't filter out
               }
               int prevT = timestampImage[x][y];
               if (prevT == DEFAULT_TIMESTAMP) {
               return false; // if there is no previous event, treat as signal event
               }
               float dt = 1e-6f * (e.timestamp - timestampImage[x][y]);
               if (dt > shotNoiseCorrelationTimeS) {
               return false; // if the previous event was too far in past, treat as signal event
               }
               numAlternatingPolarityShotNoiseEventsFilteredOut++;
               return true; // opposite polarity and follows closely after previous event, filter out
             */
        }

};

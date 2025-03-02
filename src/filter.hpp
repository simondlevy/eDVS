/*
  Abstract class for noise filtering

 Adapted from 

  https://github.com/SensorsINI/jaer/blob/master/src/net/sf/jaer/eventprocessing/filter/
    AbstractNoiseFilter.java

  Copyright (C) 2023 Simon D. Levy

  MIT License
 */

#pragma once

#include "edvs.hpp"

class AbstractNoiseFilter {

    protected:

        static const uint32_t DEFAULT_TIMESTAMP = 0;

    public:

        virtual bool check(const EDVS::event_t & e) = 0;
};

/**
 * Computes iteration range for neighborhood
 */
class NnbRange {

    public:

        uint8_t x0, x1, y0, y1;

        NnbRange(const uint8_t sigmaDistPixels=1)
        {
            _sigmaDistPixels = sigmaDistPixels;
        }

        /**
         * Computes range, fills in the fields
         *
         * @param x event location
         * @param y
         * @param ssx subsampling array size
         * @param ssy
         */
        void compute(
                const uint8_t x, const uint8_t y, const uint8_t ssx, const uint8_t ssy) 
        {

            const uint8_t d = _sigmaDistPixels;

            x0 = x < d ? 0 : x - d;
            y0 = y < d ? 0 : y - d;
            x1 = x >= ssx - d ? ssx - d : x + d;
            y1 = y >= ssy - d ? ssy - d : y + d;
        }

    private:

        uint8_t _sigmaDistPixels;
};

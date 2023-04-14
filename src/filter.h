/*
Abstract class for noise filtering

Copyright (C) 2023 Simon D. Levy

MIT License
 */

#pragma once

#include "edvs.h"

class AbstractNoiseFilter {

    protected:

        static const uint32_t DEFAULT_TIMESTAMP = 0;

    public:

        virtual bool check(const EDVS::event_t & e) = 0;
 };

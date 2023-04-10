/*
   Abstract noise-filtering class

   Copyright (C) 2023 Simon D. Levy

   MIT License
 */

#include "edvs.h"

class NoiseFilter {

    public:

        virtual void begin(void)
        {
        }

        virtual bool check(const EDVS::event_t & e) = 0;
};

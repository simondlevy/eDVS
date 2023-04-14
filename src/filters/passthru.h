/*
   Pass-through (null) noise filter for benchmarking

   Copyright (C) 2023 Simon D. Levy

   MIT License
 */

#include "edvs.h"
#include "filter.h"

class PassThruFilter : public AbstractNoiseFilter {

    public:

        virtual bool check(const EDVS::event_t & e) override
        {
            (void)e;
            return true;
        }
};

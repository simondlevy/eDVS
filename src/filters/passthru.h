/*
   Pass-through (null) noise filter for benchmarking

   Copyright (C) 2023 Simon D. Levy

   MIT License
 */

#include "edvs.h"

class PassThruFilter {

    public:

        bool check(const EDVS::event_t & e)
        {
            (void)e;
            return true;
        }
};

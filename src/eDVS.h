/*
eDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#pragma once

#include <stdint.h>

class eDVS {

    private:

        int8_t   _events[128][128];
        uint16_t _times[128][128];
        bool _done;

        void send(const char  * cmd);

    public:

        eDVS(void);

        void start(void);

        void stop(void);
};

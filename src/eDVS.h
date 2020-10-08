/*
eDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#pragma once

#include <Arduino.h>

class eDVS {

    private:

        HardwareSerial * _serial;

        int8_t   _events[128][128];
        uint16_t _times[128][128];
        bool _done;
        bool _gotx;
        uint8_t _x;

        void send(const char * cmd);

    public:

        eDVS(HardwareSerial * serial);

        void start(void);

        void stop(void);

        void update(uint8_t b);
};

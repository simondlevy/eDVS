/*
EDVS cross-platform serial support

Copyright (C) 2025 Simon D. Levy

MIT License
*/

#pragma once

#include <stdint.h>

class MySerial {

    public:

        virtual void begin(const uint32_t baud) = 0;

        virtual int available() = 0;

        virtual uint8_t read_byte() = 0;

        virtual void write_byte(const uint8_t byte) = 0;

        virtual void delay_msec(const uint32_t msec) = 0;

        virtual uint32_t time_usec() = 0;

};

/*
eDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#pragma once

#include <Arduino.h>

class eDVS {

    private:

        static const uint16_t QSIZE = 16000;

        HardwareSerial * _serial;

        bool _done;
        bool _gotx;
        uint8_t _x;

        void send(const char * cmd);

    public:

        eDVS(HardwareSerial * serial);

        void begin(uint32_t baud);

        bool hasNext(void);

        void stop(void);

        void update(uint8_t b);
};

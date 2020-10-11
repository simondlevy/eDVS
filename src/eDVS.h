/*
eDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#pragma once

#include <Arduino.h>

class eDVS {

    public:

        typedef struct {

            uint8_t  x;
            uint8_t  y;
            int8_t   p;

        } event_t;

        eDVS(HardwareSerial * serial);

        void begin(uint32_t baud);

        bool hasNext(void);

        void next(event_t & event);

        bool hasNextNext(void);

        void nextNext(event_t & event);

        void update(uint8_t b);

    private:

        static const uint16_t QSIZE = 1000;

        event_t _queue[QSIZE];
        uint16_t _qpos;

        HardwareSerial * _serial;

        bool _done;
        bool _gotx;
        uint8_t _x;

        void send(const char * cmd);

        void advance(void);
};

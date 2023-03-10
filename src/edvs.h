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

        eDVS(HardwareSerial & serial)
        {
            _serial = &serial;

            for (uint16_t k=0; k<QSIZE; ++k) {
                _queue[k].x = 0;
                _queue[k].y = 0;
                _queue[k].p = 0;
            }
            _qpos = 0;

            _gotx = false;
            _done = false;
            _x = 0;
        }

        void begin(void)
        {
            // Reset board
            send("R");

            // Enable event sending
            send("E+");

            // Use two-byte event format
            send("!E0");

            // Every other byte represents a completed event
            _x    = 0;
            _gotx = false;
        }

        void update(uint8_t b) 
        {
            // Value is in rightmost seven bits
            uint8_t v = b & 0b01111111;

            // Isolate first bit
            uint8_t f = b>>7;

            // Correct for misaligned bytes
            if (f==0 && !_gotx) {
                _gotx = !_gotx;
            }

            // Second byte; record event
            if (_gotx) {
                _queue[_qpos].x = _x; 
                _queue[_qpos].y = v; 
                _queue[_qpos].p = 2*f-1; // Convert event polarity from 0,1 to -1,+1
                advance();
            }

            // First byte; store X
            else {
                _x = v;
            }

            _gotx = !_gotx;
        }

        bool hasNext(void) 
        {
            return _queue[_qpos].p != 0; // polarity must be +1 or -1, so 0 indicates empty
        }

        void next(event_t & event)
        {
            memcpy(&event, &_queue[_qpos], sizeof(event_t));
            _queue[_qpos].p = 0;         // polarity must be +1 or -1, so 0 indicates empty
            advance();
        }

    private:

        static const uint16_t QSIZE = 1000;

        event_t _queue[QSIZE];
        uint16_t _qpos;

        HardwareSerial * _serial;

        bool _done;
        bool _gotx;
        uint8_t _x;

        void send(const char * cmd)
        {
            for (char * p=(char *)cmd; *p; p++) {
                _serial->write(*p);
            }
            _serial->write('\n');
            delay(10);
        }

        void advance(void)
        {
            _qpos = (_qpos+1) % QSIZE;
        }
};

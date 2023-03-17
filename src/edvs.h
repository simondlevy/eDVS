/*
EDVS class definition

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#pragma once

#include <Arduino.h>

class EDVS {

    private:

        static const uint32_t MAX_QSIZE = 1000;

    public:

        static const uint32_t BAUD = 2000000;

        typedef struct {

            uint8_t  x;
            uint8_t  y;
            int8_t   p;

        } event_t;

        EDVS(const uint16_t qsize=1000)
        {
            _qsize = qsize;

            for (uint16_t k=0; k<_qsize; ++k) {
                _queue[k].x = 0;
                _queue[k].y = 0;
                _queue[k].p = 0;
            }
            _qpos = 0;

            _gotx = false;
            _done = false;
            _x = 0;
        }

        void begin(HardwareSerial & serial)
        {
            // Reset board
            send(serial, "R");

            // Enable event sending
            send(serial, "E+");

            // Use two-byte event format
            send(serial, "!E0");

            // Every other byte represents a completed event
            _x    = 0;
            _gotx = false;
        }

        bool update(uint8_t b) 
        {
            auto retval = false;

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

                _current.x = _x; 
                _current.y = v; 
                _current.p = 2*f-1; // Convert event polarity from 0,1 to -1,+1

                _queue[_qpos].x = _current.x;
                _queue[_qpos].y = _current.y;
                _queue[_qpos].p = _current.p;

                advance();

                retval = true;
            }

            // First byte; store X
            else {
                _x = v;
            }

            _gotx = !_gotx;

            return retval;
        }

        bool hasNext(void) 
        {
            return _queue[_qpos].p != 0; // polarity must be +1 or -1, so 0 indicates empty
        }

        event_t next(void)
        {
            event_t event;

            event_t curr = _queue[_qpos];

            event.x = curr.x;
            event.y = curr.y;
            event.p = curr.p;

            _queue[_qpos].p = 0;         // polarity must be +1 or -1, so 0 indicates empty
            advance();

            return event;
         }

    private:

        event_t _queue[MAX_QSIZE];

        event_t _current;

        uint16_t _qsize;
        uint16_t _qpos;

        bool _done;
        bool _gotx;
        uint8_t _x;

        void send(HardwareSerial & serial, const char * cmd)
        {
            for (auto * p=(char *)cmd; *p; p++) {
                serial.write(*p);
            }
            serial.write('\n');
            delay(10);
        }

        void advance(void)
        {
            _qpos = (_qpos+1) % _qsize;
        }
};

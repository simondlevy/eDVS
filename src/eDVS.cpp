/*
eDVS class implementation

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "eDVS.h"

eDVS::eDVS(HardwareSerial * serial)
{
    _serial = serial;

    for (uint16_t k=0; k<QSIZE; ++k) {
        _queue[k].x = 0;
        _queue[k].y = 0;
        _queue[k].p = 0;
        _queue[k].t = 0;
    }
    _qpos = 0;

    _gotx = false;
    _done = false;
    _x = 0;
}

void eDVS::begin(uint32_t baud)
{
    // Begin serial communication
    _serial->begin(baud);

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

void eDVS::stop(void)
{
    _done = true;
    send("E-");
}

void eDVS::update(uint8_t b) 
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
        _queue[_qpos].t = micros(); 
        advance();
    }

    // First byte; store X
    else {
        _x = v;
    }

    _gotx = !_gotx;
}

bool eDVS::hasNext(void) 
{
    return _queue[_qpos].p != 0; // polarity must be +1 or -1, so 0 indicates empty
}

void eDVS::next(eDVS::event_t & event)
{
    memcpy(&event, &_queue[_qpos], sizeof(eDVS::event_t));
    _queue[_qpos].p = 0;         // polarity must be +1 or -1, so 0 indicates empty
    advance();
}

void eDVS::send(const char * cmd)
{
    for (char * p=(char *)cmd; *p; p++) {
        _serial->write(*p);
    }
    _serial->write('\n');
    delay(10);
}

void eDVS::advance(void)
{
    _qpos = (_qpos+1) % QSIZE;
}

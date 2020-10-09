/*
eDVS class implementation

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "eDVS.h"

eDVS::eDVS(HardwareSerial * serial)
{
    _serial = serial;
    _done = false;
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
        uint8_t y = v;
        int8_t p = 2*f-1; // Convert event polarity from 0,1 to -1,+1;
        uint32_t t = micros();
    }

    // First byte; store X
    else {
        _x = v;
    }

    _gotx = !_gotx;
}

bool eDVS::hasNext(void) 
{
    return false;
}

void eDVS::send(const char * cmd)
{
    for (char * p=(char *)cmd; *p; p++) {
        _serial->write(*p);
    }
    _serial->write('\n');
    delay(10);
}

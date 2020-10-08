/*
eDVS class implementation

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "eDVS.h"

eDVS::eDVS(HardwareSerial * serial)
{
    _serial = serial;
    bzero(_events, 128*128);
    bzero(_times , 128*128*2);
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
        _events[_x][y] = 2*f-1; // Convert event polarity from 0,1 to -1,+1;
        _times[_x][y] = millis();
    }

    // First byte; store X
    else {
        _x = v;
    }

    _gotx = !_gotx;
}

void eDVS::send(const char * cmd)
{
    for (char * p=(char *)cmd; *p; p++) {
        _serial->write(*p);
    }
    _serial->write('\n');
    delay(10);
}

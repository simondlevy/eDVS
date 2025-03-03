/*
EDVS Arduino serial support

Copyright (C) 2025 Simon D. Levy

MIT License
*/

#pragma once

#include "serial.hpp"

class ArduinoSerial : public MySerial {

    public:

        ArduinoSerial(HardwareSerial & serial)
        {
            _serial = &serial;
        }

        virtual void begin(const uint32_t baud) 
        {
            _serial->begin(baud);
        }

        virtual int available()
        {
            return _serial->available();
        }

        virtual uint8_t read_byte() 
        {
            return _serial->read();
        }

        virtual void write_byte(const uint8_t byte) 
        {
            _serial->write(byte);
        }

        virtual void delay_msec(const uint32_t msec)
        {
            delay(msec);
        }

        virtual uint32_t time_usec() 
        {
            return micros();
        }

    private:

        HardwareSerial * _serial;

};


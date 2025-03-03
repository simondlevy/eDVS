/*
EDVS POSIX serial support

Copyright (C) 2025 Simon D. Levy

MIT License
*/

#pragma once

#include <string.h>
#include <unistd.h>
#include <sys/time.h>

#include <posix-utils/serial.hpp>

#include "serial.hpp"

class PosixSerial : public MySerial {

    public:

        PosixSerial(const char * portname)
        {
            strcpy(_portname, portname);
        }

        virtual void begin(const uint32_t baud) 
        {
            _fd = openSerialPort(_portname, baud);
        }

        virtual int available()
        {
            return serial_available(_fd);
        }

        virtual uint8_t read_byte() 
        {
            uint8_t byte = 0;
            read(_fd, &byte, 1);
            return byte;
        }

        virtual void write_byte(const uint8_t byte) 
        {
           write(_fd, &byte, 1); 
        }

        virtual void delay_msec(const uint32_t msec)
        {
            usleep(msec * 1000);
        }

        virtual uint32_t time_usec() 
        {
            struct timeval time;
            gettimeofday(&time, NULL);
            return 1'000'000 * time.tv_sec + time.tv_usec;
        }

    private:

        char _portname[100];

        int _fd;
};


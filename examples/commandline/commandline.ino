/*
UART Relay program for EDVS

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.hpp"

static HardwareSerial * SERIAL_PORT = &Serial1;

void setup(void)
{
    Serial.begin(115200);

    SERIAL_PORT->begin(EDVS::BAUD);
}

void loop(void)
{
    while (Serial.available()) {
        SERIAL_PORT->write(Serial.read());
    }

    while (SERIAL_PORT->available()) {
        Serial.print((char)SERIAL_PORT->read());
    }
}

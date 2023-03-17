/*
UART Relay program for EDVS

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "edvs.h"

// For ESP32
static const uint8_t RX_PIN = 4;
static const uint8_t TX_PIN = 14;

void setup(void)
{
    Serial.begin(115200);

    // ESP32
    //Serial1.begin(2000000, SERIAL_8N1, RX_PIN, TX_PIN);

    // Ordinary Arduino
    Serial1.begin(EDVS::BAUD);
}

void loop(void)
{
    while (Serial.available()) {
        Serial1.write(Serial.read());
    }

    while (Serial1.available()) {
        Serial.print((char)Serial1.read());
    }
}

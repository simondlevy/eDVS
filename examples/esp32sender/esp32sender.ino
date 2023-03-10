/*
Stream bytes from eDVS over ESP-NOW

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"

static const uint8_t RX_PIN = 4;
static const uint8_t TX_PIN = 14;

static eDVS edvs(Serial1);

void setup(void)
{
    Serial.begin(115200);

    Serial1.begin(2000000, SERIAL_8N1, RX_PIN, TX_PIN);

    edvs.begin();
}

void loop(void)
{
    while (Serial1.available()) {
        Serial.println(Serial1.read(), HEX);
    }
}

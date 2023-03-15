/*
Streams one event at time to serial

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"

static const uint32_t BAUD = 921600;

static EDVS edvs;

void serialEvent1(void)
{
    while (Serial1.available()) {
        auto b = Serial1.read();
        edvs.update(b);
    }
}

void setup(void)
{
    Serial.begin(BAUD);

    edvs.begin(Serial1);
}

void loop(void)
{
    // Get events from DVS
    while (edvs.hasNext()) {

        // Grab event
        EDVS::event_t e = edvs.next();

        Serial.write(e.x);
        Serial.write(e.y);
        Serial.write(e.p);
    }
}

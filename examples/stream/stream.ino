/*
Single-event streaming program for Mini eDVS

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"

static EDVS edvs; 

void serialEvent1(void)
{
    while (Serial1.available()) {

        if (edvs.update(Serial1.read())) {

            EDVS::event_t e = edvs.getCurrent();

            const uint8_t coords[2] = {e.x, e.y};

            Serial.write(coords, 2);
        }
    }
}


void setup(void)
{
    Serial.begin(115200);

    Serial1.begin(EDVS::BAUD);

    edvs.begin(Serial1);
}

void loop(void)
{
}

/*
OLED display program for eDVS

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "eDVS.h"

static eDVS edvs(&Serial1);

void serialEvent1(void)
{
    while (Serial1.available()) {
        edvs.update(Serial1.read());
    }
}

void setup(void)
{
    Serial.begin(115200);
    edvs.begin(2000000);
}

void loop(void)
{
    while (edvs.hasNext()) {
        eDVS::event_t e;
        edvs.next(e);
        Serial.printf("x=%3d y=%3d p=%+d t=%d\n", e.x, e.y, e.p, e.t);
    }
    delay(1);
}

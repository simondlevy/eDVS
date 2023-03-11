/*
OLED display program for eDVS

Additional library needed: https://github.com/simondlevy/WaveshareOLED

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "edvs.h"

static eDVS edvs;

static const uint8_t EOM = 200;

void serialEvent1(void)
{
    while (Serial1.available()) {
        edvs.update(Serial1.read());
    }
}

void setup(void)
{
    Serial.begin(115200);

    Serial1.begin(2000000);

    edvs.begin(Serial1);
}

void loop(void)
{
    if (edvs.hasNext()) {

        eDVS::event_t e = edvs.next();

        Serial.write(e.x);
        Serial.write(e.y);
        Serial.write(e.p);
        Serial.write(EOM);
    }
}

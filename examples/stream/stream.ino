/*
Single-event streaming program for Mini eDVS

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"

static EDVS edvs; 

static bool ready;

void serialEvent1(void)
{
    if (Serial1.available()) {
        ready = edvs.update(Serial1.read());
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
    static uint32_t count;

    if (ready) {
        ready = false;
        auto e = edvs.getCurrent();
        count++;
    }

    static uint32_t msec_prev;

    auto msec_curr = millis();

    if (msec_curr - msec_prev > 1000) {
        Serial.println(count);
        count = 0;
        msec_prev = msec_curr;
    }
}

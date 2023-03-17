/*
Frames-based display program for EDVS

Additional library needed: https://github.com/simondlevy/WaveshareOLED

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "edvs.h"

static const uint32_t BAUD = 921600;

static uint32_t FPS = 120;

static const uint32_t MAX_EVENTS_PER_FRAME = 1250;

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

    Serial1.begin(EDVS::BAUD);

    edvs.begin(Serial1);
}

void loop(void)
{
    static uint32_t count;

    static uint8_t frame[2 * MAX_EVENTS_PER_FRAME];

    // Get events from DVS
    while (edvs.hasNext()) {

        // Grab event
        EDVS::event_t e = edvs.next();

        frame[count]   = e.x;
        frame[count+1] = e.y; 

        count += 2;
    }

    static uint32_t usec_prev;

    auto usec = micros();

    if (usec - usec_prev > 1000000/FPS) {
        usec_prev = usec;
        Serial.write(frame, count);
        count = 0;
        memset(frame, 0, sizeof(frame));
    }
}

/*
OLED display program for eDVS

Additional library needed: https://github.com/simondlevy/WaveshareOLED

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "edvs.h"
#include <OLED_GFX.h>

// OLED Pins
static const uint8_t CS  = 10;
static const uint8_t DC  = 9;
static const uint8_t RST = 8;

// Queue of old events for erasing
static const uint16_t QSIZE = 1000;
static eDVS::event_t queue[QSIZE];
static uint16_t qpos;

OLED_GFX oled(CS, DC, RST);

static eDVS edvs;

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

    oled.begin();

    oled.Clear_Screen();

    qpos = 0;
}

void loop(void)
{
    static uint8_t maxval;

    // Get events from DVS
    if (edvs.hasNext()) {

        // Display event
        eDVS::event_t e = edvs.next();
        oled.Set_Color(e.p == -1 ? OLED_GFX::GREEN : OLED_GFX::RED);
        oled.Draw_Pixel(e.y,e.x);

        // Store event in queue
        queue[qpos].x = e.x;
        queue[qpos].y = e.y;
        qpos = (qpos + 1) % QSIZE;

        if (e.x > maxval) {
            maxval = e.x;
        }
        if (e.y > maxval) {
            maxval = e.y;
        }

    }

    // Remove pixel for oldest event in queue
    eDVS::event_t e2 = queue[(qpos+1)%QSIZE];
    oled.Set_Color(OLED_GFX::BLACK);
    oled.Draw_Pixel(e2.y,e2.x);
}

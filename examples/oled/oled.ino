/*
OLED display program for EDVS

Additional library needed: https://github.com/simondlevy/WaveshareOLED

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "edvs.h"
#include <OLED_GFX.h>

// End-Of-Message byte
static const uint8_t EOM = 200;

// OLED Pins
static const uint8_t CS  = 10;
static const uint8_t DC  = 9;
static const uint8_t RST = 8;

// Queue of old events for erasing
static const uint16_t QSIZE = 1000;
static EDVS::event_t queue[QSIZE];
static uint16_t qpos;

OLED_GFX oled(CS, DC, RST);

static EDVS edvs;

static bool ready;

void serialEvent1(void)
{
    while (Serial1.available()) {
        ready = edvs.update(Serial1.read());
    }
}

void setup(void)
{

    Serial1.begin(EDVS::BAUD);

    edvs.begin(Serial1);

    oled.begin();

    oled.Clear_Screen();

    qpos = 0;
}

void loop(void)
{
    // Get events from DVS
    //if (edvs.hasNext()) {
    if (ready) {

        ready = false;

        // Grab event
        EDVS::event_t e = edvs.getCurrent();

        // Display it
        oled.Set_Color(e.p == -1 ? OLED_GFX::GREEN : OLED_GFX::RED);
        oled.Draw_Pixel(e.y,e.x);

        // Store it in the queue
        queue[qpos].x = e.x;
        queue[qpos].y = e.y;
        qpos = (qpos + 1) % QSIZE;
    }

    // Erase pixel for oldest event in queue
    EDVS::event_t e2 = queue[(qpos+1)%QSIZE];
    oled.Set_Color(OLED_GFX::BLACK);
    oled.Draw_Pixel(e2.y,e2.x);
}

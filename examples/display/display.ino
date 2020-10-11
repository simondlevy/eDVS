/*
OLED display program for eDVS

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "eDVS.h"
#include <OLED_GFX.h>

// OLED Pins
static const uint8_t CS  = 10;
static const uint8_t DC  = 9;
static const uint8_t RST = 8;

typedef struct {
    uint8_t x;
    uint8_t y;
    uint32_t t;
} event_t;

static const uint16_t QSIZE = 1000;
static event_t queue[QSIZE];
static uint16_t qpos;

OLED_GFX oled(CS, DC, RST);

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

    oled.begin();

    oled.Clear_Screen();

    qpos = 0;
}

void loop(void)
{
    // Get events from DVS, storing times and pixels
    if (edvs.hasNext()) {

        eDVS::event_t e;
        edvs.next(e);
        oled.Set_Color(e.p == -1 ? OLED_GFX::GREEN : OLED_GFX::RED);
        oled.Draw_Pixel(e.y,e.x);

        queue[qpos].x = e.x;
        queue[qpos].y = e.y;
        queue[qpos].t = millis();
        qpos = (qpos + 1) % QSIZE;

    }

    event_t e2 = queue[(qpos+1)%QSIZE];
    if (e2.t > 0 /*&& (millis() - e2.t) > 1*/) {
        oled.Set_Color(OLED_GFX::BLACK);
        oled.Draw_Pixel(e2.y,e2.x);
        e2.t = 0;
    }
}

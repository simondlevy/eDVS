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

OLED_GFX oled(CS, DC, RST);

class SparseMatrix {

    private:

        typedef struct {

            uint8_t x;
            uint8_t y;
        } coords;

        uint32_t a[128][128];

        uint8_t t[128*128];
};

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

}

void loop(void)
{

    while (edvs.hasNext()) {

        eDVS::event_t e;
        edvs.next(e);
        oled.Draw_Pixel(e.x,e.y);
        oled.Set_Color(e.p == -1 ? OLED_GFX::GREEN : OLED_GFX::RED);
    }

    delay(1);
}

/*
OLED display program for eDVS

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "eDVS.h"
#include "SparseMatrix.hpp"
#include <OLED_GFX.h>

// Milliseconds before event "ages out" from display
static const uint32_t AGEOUT = 100;

// OLED Pins
static const uint8_t CS  = 10;
static const uint8_t DC  = 9;
static const uint8_t RST = 8;

OLED_GFX oled(CS, DC, RST);

static eDVS edvs(&Serial1);

class AgeMatrix : public SparseMatrix {

    public:

        virtual void fun(uint8_t x, uint8_t y) override
        {
            if ((millis()-get(x, y)) > AGEOUT) {
                oled.Draw_Pixel(y,x);
            }
        }
};

AgeMatrix ages;

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
    // Get events from DVS, storing times and pixels
    while (edvs.hasNext()) {

        eDVS::event_t e;
        edvs.next(e);
        oled.Set_Color(e.p == -1 ? OLED_GFX::GREEN : OLED_GFX::RED);
        oled.Draw_Pixel(e.y,e.x);
        ages.put(e.x, e.y, millis());
    }

    delay(25);

    // Zero out pixels with events older than a certain time before now
    oled.Set_Color(OLED_GFX::BLACK);
    ages.forall();

    delay(25);
}

/*
Single-event streaming program for Mini eDVS

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"
#include "filters/knoise.h"
#include "filters/passthru.h"

static EDVS edvs; 

static OrderNbackgroundActivityFilter filter;
//static PassThruFilter filter;

void serialEvent1(void)
{
    while (Serial1.available()) {

        if (edvs.update(Serial1.read())) {

            EDVS::event_t e = edvs.getCurrent();

            if (filter.check(e)) {
                const uint8_t coords[2] = {e.x, e.y};
                Serial.write(coords, 2);
            }
        }
    }
}


void setup(void)
{
    Serial.begin(115200);

    edvs.begin(Serial1);
}

void loop(void)
{
}

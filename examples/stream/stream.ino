/*
Single-event streaming program for Mini eDVS

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"
#include "filters/knoise.h"
#include "filters/passthru.h"

static EDVS edvs = EDVS(Serial1); 

//static OrderNbackgroundActivityFilter filter;
static PassThruFilter filter;

void setup(void)
{
    Serial.begin(115200);

    edvs.begin();
}

void loop(void)
{
    if (edvs.update()) {

        EDVS::event_t e = edvs.getCurrent();

        if (filter.check(e)) {

            Serial.write(e.x);
            Serial.write(e.y);
        }
    }
}

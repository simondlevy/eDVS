/*
Single-event streaming program for Mini eDVS

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"
#include "filters/passthru.h"
#include "filters/onf.h"
#include "filters/stcf.h"

static EDVS edvs = EDVS(Serial1); 

//static PassThruFilter filter;
//static OrderNbackgroundActivityFilter filter;
static SpatioTemporalCorrelationFilter filter;

void setup(void)
{
    Serial.begin(115200);

    edvs.begin();
}

void loop(void)
{
    static uint8_t frame[4096];
    static uint32_t index;

    if (edvs.update()) {

        EDVS::event_t e = edvs.getCurrent();

        if (filter.check(e)) {

            frame[index]   = e.x;
            frame[index+1] = e.y;

            index += 2;

            if (index == 4096) {

                Serial.write(frame, 4096);

                memset(frame, 0, 4096);
                index = 0;
            }
        }
    }
}

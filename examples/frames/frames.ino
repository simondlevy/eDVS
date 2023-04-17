/*
   Single-event streaming program for Mini eDVS

   Copyright (C) 2023 Simon D. Levy

   MIT License
 */

#include "edvs.h"
#include "filters/passthru.h"
#include "filters/onf.h"
#include "filters/stcf.h"
#include "timertask.h"

static const uint32_t FRAME_SIZE = 4096;

static const uint32_t FRAMES_PER_SECOND = 30;

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
    static uint8_t frame[FRAME_SIZE];
    static uint32_t index;

    static TimerTask task;

    if (edvs.update()) {

        EDVS::event_t e = edvs.getCurrent();

        if (filter.check(e)) {

            frame[index]   = e.x;
            frame[index+1] = e.y;

            index = (index + 2) % FRAME_SIZE;
        }
    }

    if (task.ready(FRAMES_PER_SECOND)) {

        Serial.write(frame, FRAME_SIZE);
        memset(frame, 0, FRAME_SIZE);
    }
}

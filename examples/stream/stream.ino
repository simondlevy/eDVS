/*
Single-event streaming program for Mini eDVS

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include <arduino_serial.hpp>
#include <edvs.hpp>
#include <filters/passthru.hpp>
#include <filters/knoise.hpp>
#include <filters/stcf.hpp>

static ArduinoSerial serial = ArduinoSerial(Serial1);

static EDVS edvs = EDVS(serial);

//static PassThruFilter filter;
//static Knoise filter;
static SpatioTemporalCorrelationFilter filter;

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

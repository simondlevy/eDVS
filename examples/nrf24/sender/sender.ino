/*
Single-event streaming program for Mini eDVS

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include <RF24.h>

#include "edvs.h"
#include "filters/knoise.h"
#include "filters/passthru.h"

static const uint8_t CE_PIN = 9;

static const uint32_t RADIO_FREQ = 18000000;

static const byte RADIO_ADDRESS[6] = "00001";

static RF24 radio(CE_PIN, SS, RADIO_FREQ); // use builtin chip-select pin SS

static EDVS edvs; 

static OrderNbackgroundActivityFilter filter;
//static PassThruFilter filter;

static void startRadio(void)
{
    radio.begin();
    radio.setDataRate(RF24_2MBPS );
    radio.openWritingPipe(RADIO_ADDRESS);
    radio.setPALevel(RF24_PA_HIGH);
    radio.stopListening();
}

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

    startRadio();

    edvs.begin(Serial1);
}

void loop(void)
{
    uint8_t buf[32] = {};
    for (uint8_t k=0; k<sizeof(buf); ++k) {
        buf[k] = k;
    }
    radio.write(buf, sizeof(buf));
}

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

static EDVS edvs = EDVS(Serial1); 

static Knoise filter;
// static PassThruFilter filter;

static void startRadio(void)
{
    radio.begin();
    radio.setDataRate(RF24_2MBPS );
    radio.openWritingPipe(RADIO_ADDRESS);
    radio.setPALevel(RF24_PA_HIGH);
    radio.stopListening();
}

static uint32_t report(uint32_t count)
{
    static uint32_t usec_prev;

    auto usec = micros();

    if (usec - usec_prev > 1000000) {

        if (usec_prev > 0) {
            printf("%06d events / second\n", count);
        }

        usec_prev = usec;
        count = 0;
    }

    return count;
}

void setup(void)
{
    Serial.begin(115200);

    startRadio();

    edvs.begin();
}

void loop(void)
{
    static uint8_t buf[32];
    static uint8_t buf_index;

    static uint32_t event_count;

    if (edvs.update()) {

        EDVS::event_t e = edvs.getCurrent();

        if (filter.check(e)) {
            buf[buf_index] = e.x;
            buf[buf_index+1] = e.y;
            buf_index += 2;
            event_count++;
        }
    }

    if (buf_index == sizeof(buf)) {
        radio.write(buf, sizeof(buf));
        buf_index = 0;
    }

    event_count = report(event_count);
}

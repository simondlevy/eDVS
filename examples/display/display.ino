/*
OLED display program for eDVS

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include "eDVS.h"

static eDVS edvs(&Serial1);

static uint32_t count;

void serialEvent1(void)
{
    count++;
}

void setup(void)
{
    count = 0;
    Serial.begin(115200);
    edvs.begin(2000000);
}

void loop(void)
{
    Serial.println(count);
    delay(1);
}

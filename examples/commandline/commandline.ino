/*
Command-line interaction with eDVS

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"

static eDVS edvs(Serial1);

void serialEvent1(void)
{
    while (Serial1.available()) {
        edvs.update(Serial1.read());
    }
}

void setup(void)
{
    Serial.begin(115200);

    Serial1.begin(2000000);

    edvs.begin();
}

void loop(void)
{
}

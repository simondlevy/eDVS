/*
JPEG encoding for EDVS

Additional library needed: https://github.com/bitbank2/JPEGENC

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"
#include "edvs_jpeg.h"

#include <JPEGENC.h>

static EDVS edvs;

void serialEvent1(void)
{
    while (Serial1.available()) {
        auto b = Serial1.read();
        edvs.update(b);
    }
}

static int32_t write(JPEGFILE *p, uint8_t *buffer, int32_t length) 
{
    (void)p;

    return Serial.write(buffer, length);
}

void setup() 
{
    Serial.begin(115200);

    edvs.begin(Serial1);
} 

void loop() 
{
    EdvsJpeg::step(edvs, write);
}

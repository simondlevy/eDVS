/*
OLED display program for eDVS

Additional library needed: https://github.com/bitbank2/JPEGENC

Copyright (C) 2020 Simon D. Levy

MIT License
*/

#include <JPEGENC.h>

static JPEGENCODE jpe;
static JPEG jpg;

static uint8_t image[128*128];

void setup(void)
{
    Serial.begin(115200);

    for (uint8_t k=0; k<128; ++k) {
        image[k*128+k] = 255;
    }
}

void loop(void)
{
    auto rc = jpg.encodeBegin(
            &jpe, 128, 128, JPEG_PIXEL_GRAYSCALE, JPEG_SUBSAMPLE_444, JPEG_Q_HIGH);

    if (rc == JPEG_SUCCESS) {
        Serial.println(micros());
    }
}

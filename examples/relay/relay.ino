/*
Relay program for eDVS

Copyright (C) 2020 Simon D. Levy

MIT License
*/

void setup(void)
{
    Serial.begin(115200);
    delay(1000);
}

void loop(void)
{
    static uint8_t x;
    static uint8_t y;

    x = (x+1) % 128;

    Serial.write(y);
    Serial.write(x);

    //Serial.write(0x99);
}

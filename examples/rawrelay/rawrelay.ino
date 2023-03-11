/*
UART Relay program for eDVS

Copyright (C) 2020 Simon D. Levy

MIT License
*/

void setup(void)
{
    Serial.begin(2000000);

    Serial1.begin(2000000);
}

void loop(void)
{
    while (Serial.available()) {
        Serial1.write(Serial.read());
    }

    while (Serial1.available()) {
        Serial.print((char)Serial1.read());
    }
}

/*
Test ESP32 UART at maximum Baud rate

Copyright (C) 2020 Simon D. Levy

MIT License
*/

static const uint8_t SERIAL1_RX = 32;
static const uint8_t SERIAL1_TX = 33; // unused

static const uint32_t BAUD = 4000000;

static uint32_t start;
static uint32_t prev;

void setup(void)
{
    Serial.begin(115200);

    Serial1.begin(BAUD, SERIAL_8N1, SERIAL1_RX, SERIAL1_TX);

    start = millis();
}

void loop(void)
{
    static const uint8_t BUFSIZE = 30;

    static char buf[BUFSIZE];
    static uint8_t bufidx;

    if (Serial1.available()) {
        char c = Serial1.read();
        buf[bufidx] = c;
        bufidx = (bufidx+1) % BUFSIZE;
    }

    uint32_t time = (millis()-start) / 1000;

    if (time > prev) {
        for (uint8_t k=0; k<bufidx; ++k) {
            Serial.print(buf[k]);
        }
        Serial.println();
        prev = time;
    }
}

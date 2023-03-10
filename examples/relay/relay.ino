/*
UART Relay program for eDVS

Copyright (C) 2020 Simon D. Levy

MIT License
*/

// For ESP32
static const uint8_t RX_PIN = 4;
static const uint8_t TX_PIN = 14;

void setup(void)
{
    Serial.begin(2000000);

    // ESP32
    Serial1.begin(2000000, SERIAL_8N1, RX_PIN, TX_PIN);

    // Ordinary Arduino
    // Serial1.begin(2000000, SERIAL_8N1, RX_PIN, TX_PIN);
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

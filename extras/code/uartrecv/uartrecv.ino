static const uint8_t SERIAL1_RX = 32;
static const uint8_t SERIAL1_TX = 33; // unused

static const uint32_t BAUD = 230400;

void setup(void)
{
    Serial.begin(BAUD);

    Serial1.begin(BAUD, SERIAL_8N1, SERIAL1_RX, SERIAL1_TX);

}

void loop(void)
{
    while (Serial1.available()) {
        Serial.println((char)Serial1.read());
    }
}

static const uint8_t SERIAL1_RX = 32;
static const uint8_t SERIAL1_TX = 33; // unused

void setup(void)
{
    Serial.begin(115200);

    Serial1.begin(115000, SERIAL_8N1, SERIAL1_RX, SERIAL1_TX);

}

void loop(void)
{
    while (Serial1.available()) {
        Serial.println(Serial1.read());
    }
}

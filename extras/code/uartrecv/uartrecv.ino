static const uint8_t SERIAL1_RX = 32;
static const uint8_t SERIAL1_TX = 33; // unused

static const uint32_t BAUD = 2000000;

static uint32_t start;
static uint32_t count;
static uint32_t prev;

void setup(void)
{
    Serial.begin(115200);

    Serial1.begin(BAUD, SERIAL_8N1, SERIAL1_RX, SERIAL1_TX);

    start = millis();
    count = 0;
}

void loop(void)
{
    if (Serial1.available()) {
        char c = Serial1.read();
        if (c==65) {
            count+=26;
        }
    }

    uint32_t time = (millis()-start) / 1000;

    if (time > prev) {
        Serial.println(count);
        count = 0;
        prev = time;
    }
}

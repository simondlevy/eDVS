#include <RF24.h>

static const uint8_t CE_PIN = 7;
static const uint8_t CS_PIN = 8;

static RF24 radio(CE_PIN, CS_PIN, 18000000);

static const byte ADDRESS[6] = "00001";

void setup() 
{
    Serial.begin(115200);

    radio.begin();
    radio.setDataRate( RF24_2MBPS );
    radio.openReadingPipe(0, ADDRESS);
    radio.setPALevel(RF24_PA_HIGH);
    radio.startListening();
}

void loop() 
{
    static uint32_t count;
    static uint8_t buf[32] = {};

    while (radio.available()) {
        radio.read(buf, sizeof(buf));
        count += sizeof(buf);
    }

    static uint32_t usec_prev;
    auto usec = micros();
    if (usec - usec_prev > 1000000) {
        if (usec_prev > 0) {
            printf("%06d events / second:", count/2);
            for (uint8_t k=0; k<sizeof(buf); ++k) {
                printf(" %03d", buf[k]);
            }
            printf("\n");
        }
        usec_prev = usec;
        count = 0;
    }
}

#include "edvs.h"
#include <JPEGENC.h>

static const uint32_t FPS = 30;

static eDVS edvs;

void serialEvent1(void)
{
    while (Serial1.available()) {
        auto b = Serial1.read();
        edvs.update(b);
    }
}

// JPEG compression functions =================================================

static void * myOpen(const char *filename) 
{
    (void)filename;
    return (void *)1; // non-NULL value
}

static void myClose(JPEGFILE *p) 
{
    (void)p;
}

static int32_t myRead(JPEGFILE *p, uint8_t *buffer, int32_t length) 
{
    (void)p;
    (void)buffer;
    return length;
}

static int32_t myWrite(JPEGFILE *p, uint8_t *buffer, int32_t length) 
{
    return Serial.write(buffer, length);
}

static int32_t mySeek(JPEGFILE *p, int32_t position) 
{
    (void)p;
    return position;
}

// ============================================================================

void setup() 
{
    Serial.begin(115200);

    Serial1.begin(2000000);

    edvs.begin(Serial1);
} 

static void sendImage(void)
{
    static const uint32_t SIZE = 128;

    JPEGENCODE jpe;
    JPEG jpg;

    auto rc = jpg.open("/TEST.JPG", myOpen, myClose, myRead, myWrite, mySeek);

    uint8_t bitmap[SIZE*SIZE];

    static uint8_t pixpos;

    if (rc == JPEG_SUCCESS) {

        auto rc = jpg.encodeBegin(
                &jpe, SIZE, SIZE, JPEG_PIXEL_GRAYSCALE, JPEG_SUBSAMPLE_444, JPEG_Q_HIGH);

        const auto iMCUCount = ((SIZE + jpe.cx-1)/ jpe.cx) * ((SIZE + jpe.cy-1) / jpe.cy);

        if (rc == JPEG_SUCCESS) {

            memset(bitmap, 0, sizeof(bitmap));

            bitmap[63 + pixpos] = 255;

            pixpos = (pixpos + 1) % 128;

            for (uint32_t i=0; i<iMCUCount && rc == JPEG_SUCCESS; i++) {
                rc = jpg.addMCU(&jpe, &bitmap[jpe.x + (jpe.y * SIZE)], SIZE);
            }

            jpg.close();
        } 
    } 
}

void loop() 
{
    static uint32_t usec_prev;

    auto usec = micros();

    if (usec - usec_prev > 1000000/FPS) {
        sendImage();
        usec_prev = usec;
    }
}

#include "edvs.h"
#include <JPEGENC.h>

static const uint32_t IMGSIZE = 128;

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

static void sendImage(uint8_t pixels[])
{
    JPEGENCODE jpe;
    JPEG jpg;

    auto rc = jpg.open("/TEST.JPG", myOpen, myClose, myRead, myWrite, mySeek);

    if (rc == JPEG_SUCCESS) {

        auto rc = jpg.encodeBegin(
                &jpe, IMGSIZE, IMGSIZE, JPEG_PIXEL_GRAYSCALE, JPEG_SUBSAMPLE_444, JPEG_Q_HIGH);

        const auto iMCUCount = ((IMGSIZE + jpe.cx-1)/ jpe.cx) * ((IMGSIZE + jpe.cy-1) / jpe.cy);

        if (rc == JPEG_SUCCESS) {

            for (uint32_t i=0; i<iMCUCount && rc == JPEG_SUCCESS; i++) {
                rc = jpg.addMCU(&jpe, &pixels[jpe.x + (jpe.y * IMGSIZE)], IMGSIZE);
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

        static uint8_t pixpos;
        static uint8_t pixels[IMGSIZE*IMGSIZE];

        pixpos = (pixpos + 1) % 128;
        pixels[63 + pixpos] = 255;
        pixpos = (pixpos + 1) % 128;
        sendImage(pixels);
        memset(pixels, 0, sizeof(pixels));

        usec_prev = usec;
    }
}

/*
 * Adapted from https://github.com/bitbank2/JPEGENC/blob/master/examples/jpeg_encode_perf/jpeg_encode_perf.ino
 */

#include <JPEGENC.h>

static const uint32_t FPS = 30;

// Callback functions needed by the unzipLIB to access a file system
// The library has built-in code for memory-to-memory transfers, but needs
// these callback functions to allow using other storage media
//
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


void setup() 
{
    Serial.begin(115200);
} 

void loop() 
{
    static const uint32_t SIZE = 128;

    JPEGENCODE jpe;
    JPEG jpg;

    uint8_t ucMCU[SIZE];

    auto rc = jpg.open("/TEST.JPG", myOpen, myClose, myRead, myWrite, mySeek);

    if (rc == JPEG_SUCCESS) {

        auto rc = jpg.encodeBegin(
                &jpe, SIZE, SIZE, JPEG_PIXEL_GRAYSCALE, JPEG_SUBSAMPLE_444, JPEG_Q_HIGH);

        if (rc == JPEG_SUCCESS) {

            memset(ucMCU, 0, sizeof(ucMCU));

            auto iMCUCount = ((SIZE + jpe.cx-1)/ jpe.cx) * ((SIZE + jpe.cy-1) / jpe.cy);

            for (uint32_t i=0; i<iMCUCount && rc == JPEG_SUCCESS; i++) {

                for (int j=0; j<8; j++) {
                    ucMCU[j*8+j] = 255;
                }

                rc = jpg.addMCU(&jpe, ucMCU, 8);
            }

            jpg.close();

            delayMicroseconds(1000000/FPS);
        }
    } // opened successfully
}

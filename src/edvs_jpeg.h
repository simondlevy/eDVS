/*
JPEG encoding for EDVS

Additional library needed: https://github.com/bitbank2/JPEGENC

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include "edvs.h"
#include <JPEGENC.h>

class EdvsJpeg {

    private:

        static const uint32_t IMGSIZE = 128;
        static const uint32_t FPS = 30;
        static const uint8_t NEGATIVE_EVENT_GRAYSCALE = 100;
        static const uint8_t POSITIVE_EVENT_GRAYSCALE = 200;

        static void * open(const char *filename) 
        {
            (void)filename;
            return (void *)1; // non-NULL value
        }

        static void close(JPEGFILE *p) 
        {
            (void)p;
        }

        static int32_t read(JPEGFILE *p, uint8_t *buffer, int32_t length) 
        {
            (void)p;
            (void)buffer;
            return length;
        }

        static int32_t seek(JPEGFILE *p, int32_t position) 
        {
            (void)p;
            return position;
        }

        static void sendImage(
                uint8_t pixels[],
                int32_t (*writefun)(JPEGFILE *p, uint8_t *buffer, int32_t length)) 
        {
            JPEGENCODE jpe;
            JPEG jpg;

            auto rc = jpg.open("/TEST.JPG", open, close, read, writefun, seek);

            if (rc == JPEG_SUCCESS) {

                auto rc = jpg.encodeBegin(
                        &jpe,
                        IMGSIZE,
                        IMGSIZE,
                        JPEG_PIXEL_GRAYSCALE,
                        JPEG_SUBSAMPLE_444,
                        JPEG_Q_HIGH);

                const auto iMCUCount =
                    ((IMGSIZE + jpe.cx-1)/ jpe.cx) * ((IMGSIZE + jpe.cy-1) / jpe.cy);

                if (rc == JPEG_SUCCESS) {

                    for (uint32_t i=0; i<iMCUCount && rc == JPEG_SUCCESS; i++) {
                        rc = jpg.addMCU(&jpe, &pixels[jpe.x + (jpe.y * IMGSIZE)], IMGSIZE);
                    }

                    jpg.close();
                } 
            } 
        }

    public:

        static void step(
                EDVS & edvs,
                int32_t (*writefun)(JPEGFILE *p, uint8_t *buffer, int32_t length)) 
        {
            static uint32_t usec_prev;

            auto usec = micros();

            if (usec - usec_prev > 1000000/FPS) {

                uint8_t pixels[IMGSIZE*IMGSIZE];

                memset(pixels, 0, sizeof(pixels));

                while (edvs.hasNext()) {
                    EDVS::event_t e = edvs.next();
                    pixels[e.x * IMGSIZE + e.y] =
                        e.p == -1 ?
                        NEGATIVE_EVENT_GRAYSCALE :
                        POSITIVE_EVENT_GRAYSCALE;
                }

                sendImage(pixels, writefun);

                usec_prev = usec;
            }
        }
};

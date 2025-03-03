/*
Single-event streaming program for Mini eDVS

Copyright (C) 2023 Simon D. Levy

MIT License
*/

#include <posix_serial.hpp>
#include <edvs.hpp>
#include <filters/passthru.hpp>

int main(int argc, char ** argv)
{
    PosixSerial serial = PosixSerial("/dev/ttyS0");

    EDVS edvs = EDVS(serial);

    PassThruFilter filter;
    //static Knoise filter;
    //static SpatioTemporalCorrelationFilter filter;

    edvs.begin();

    while (true) {
        {
            if (edvs.update()) {

                EDVS::event_t e = edvs.getCurrent();

                if (filter.check(e)) {

                    printf("%d %d\n", e.x, e.y);

                    //write(stdout, e.x);
                    //write(stdout, e.y);
                }
            }
        }
    }
}

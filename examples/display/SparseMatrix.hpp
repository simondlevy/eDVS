/*
Simple sparse matrix class

Copyright (C) 2020 Simon D. Levy

MIT License
*/

class SparseMatrix {

    private:

        typedef struct {
            uint8_t x;
            uint8_t y;
        } coords_t;

        static const uint8_t SIZE = 128;

        uint32_t _vals[SIZE][SIZE];

        coords_t _nonzero[SIZE*SIZE];

        uint16_t _nzcount;

    public:

        SparseMatrix(void) 
        {
            bzero(_vals, SIZE*SIZE*4);
            bzero(_nonzero, SIZE*SIZE*sizeof(coords_t));
            _nzcount = 0;
        }

        void put(uint8_t x, uint8_t y, uint32_t val) 
        {
            if (!_vals[x][y]) {
                _nonzero[_nzcount].x = x;
                _nonzero[_nzcount].y = y;
                _nzcount++;
            }

            _vals[x][y] = val;
        }

        uint32_t get(uint8_t x, uint8_t y)
        {
            return _vals[x][y];
        }

        virtual void fun(uint8_t x, uint8_t y) = 0;

        void forall(void) 
        {
            for (uint32_t k=0; k<_nzcount; ++k) {
                coords_t c = _nonzero[k];
                fun(c.x, c.y);
            }
        }
};

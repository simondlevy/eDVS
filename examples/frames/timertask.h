class TimerTask {

    public:

        bool ready(const uint32_t freq_hz)
        {
            auto usec_curr = micros();

            bool result = false;

            if (usec_curr - _usec_prev > 1000000/freq_hz) {

                if (_usec_prev > 0) {
                    result = true;
                }

                _usec_prev = usec_curr;
            }        

            return result;
        }

    private:

        uint32_t _usec_prev;
};

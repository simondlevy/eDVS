SKETCH = stream

BOARD = teensy:avr:teensy41

PORT = /dev/ttyACM0

build: $(SKETCH).cpp
	g++ -o $(SKETCH) -Wall -I$(HOME)/Desktop -I../src $(SKETCH).cpp

flash:
	arduino-cli upload -p $(PORT) --fqbn $(BOARD) .

clean:
	rm -rf obj

edit:
	vim $(SKETCH).cpp

listen:
	miniterm.py $(PORT) 115200

display:
	./playstream.py


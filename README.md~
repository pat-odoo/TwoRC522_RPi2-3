# TwoRC522_RPi2-3
Two RFID readers with Raspberry Pi

Assuming the python-dev and SPI-Py libraries are already correctly installed, configured, and tested on Raspberry Pi.

Otherwise, here is a brief help:
```{r, engine='bash', count_lines}
$ sudo apt-get install python-dev
$ git clone https://github.com/lthiery/SPI-Py.git
$ cd SPI-Py
$ sudo python setup.py install
```

Download: 
```{r, engine='bash', count_lines}
$ git clone https://github.com/pat-odoo/TwoRC522_RPi2-3.git
```
Use:
Create Two Instance of the same Library. (Ex. 1-TwoRC522_RPi2-3 and 2-TwoRC522_RPi2-3).

Change Line 46 in card_reader.py file.

In File 1-TwoRC522_RPi2-3 :- 'MIFAREReader = MFRC522(self.RST1, self.SPI_DEV0)'

In File 2-TwoRC522_RPi2-3 :- 'MIFAREReader = MFRC522(self.RST2, self.SPI_DEV1)'

Terminal-1:
```{r, engine='bash', count_lines}
$ cd 1-TwoRC522RPi/
$ sudo python run_main_test.py 
```

Terminal-2:
```{r, engine='bash', count_lines}
$ cd 2-TwoRC522RPi/
$ sudo python run_main_test.py 
```
Press Ctrl + z to finish.

![alt tag](https://camo.githubusercontent.com/e715575770d278577ca75e0c050ff7e8394b410c/68747470733a2f2f7777772e72617370626572727970692e6f72672f666f72756d732f646f776e6c6f61642f66696c652e7068703f69643d3136353237)

Credits :

https://github.com/lthiery/SPI-Py. - MontaVista Software, Inc., Anton Vorontsov(2007)

Repository of the original class: https://github.com/mxgxw/MFRC522-python. - Mario Gómez

Two RC522 Concept: https://github.com/erivandoramos/TwoRC522RPi

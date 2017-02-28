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
Create Two Instance of the same Library. (Ex. 1-TwoRC522_RPi2-3 and 2-TwoRC522_RPi2-3)
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

![alt tag](https://drive.google.com/open?id=0Bz4EDmux79M7QVp5T2FEX1lOUGM)

Credits :

https://github.com/lthiery/SPI-Py. - MontaVista Software, Inc., Anton Vorontsov(2007)
Repository of the original class: https://github.com/mxgxw/MFRC522-python. - Mario Gómez
Two RC522 Concept: https://github.com/erivandoramos/TwoRC522RPi

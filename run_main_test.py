#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class in Python 2.7 for testing two RFID readers with Raspberry Pi.

Use: 
$ cd TwoRC522RPi/
$ sudo python run_main_test.py 
Press Ctrl + z to finish.

"""

import sys
from module.card_reader import CardReader

def main(self):
    
    card_reader = CardReader()
    try:
        card_reader.start()
    except KeyboardInterrupt:
        print "trl+C received! Sending kill to " + reader_card.getName()
        if reader_card.isAlive():
            reader_card._stopevent.set()
            
if __name__ == '__main__':
    main(sys.argv)
  
    
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classe em Python 2.7 para controle das portas GPIO (BCM) do Raspberry Pi versões RPi B+, RPi 2B e RPi 3B.

"""

import os
import yaml
from module.gpio import PinsGPIO


PINS_YML = os.path.join(os.path.dirname(os.path.abspath(__file__)),"pins.yml")

class PinControl(PinsGPIO):
    
    print "GPIO v." + str(PinsGPIO().gpio.VERSION)

    def __init__(self):
        super(PinControl, self).__init__()
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setwarnings(False)
        self.load_yaml()

    def load_yaml(self):
        try:
            with open(PINS_YML) as file_data:
                self.pins = yaml.safe_load(file_data)
        except Exception as e:
            print e

    def pin_response(self, num, config):
        try:
            output = {
                'name': config.get('name'),
                'gpio': num,
                'mode': config.get('mode'),
                'state': self.gpio.input(num)
            }
            resistor = config.get('resistor')
            if resistor:
                output['resistor'] = resistor
            return output
        except Exception as e:
            print e
            
    def updates(self, num, value):   
        pin_number = int(num)
        try:
            self.pins[pin_number]
            self.gpio.output(pin_number, value)
            state = self.gpio.input(pin_number)
            return state
        except Exception as e:
            print e
            
    def state(self, num):      
        pin_number = int(num)
        try:
            state = self.gpio.input(pin_number)
            return state
        except Exception as e:
            print e
        
    def read(self, number):    
        pin_number = int(number)
        pin_enabled = None
        try:
            pin_config = self.pins[pin_number]
            if pin_config['mode'] == 'OUT':
                self.gpio.setup(pin_config['gpio'], self.gpio.OUT)
                print pin_config['name']
            if pin_config['mode'] == 'IN':
                self.gpio.setup(pin_config['gpio'], self.gpio.IN, pull_up_down= self.gpio.PUD_UP if pin_config['resistor'] == 'PUD_UP' else self.gpio.PUD_DOWN)
                print pin_config['name']
            pin_enabled = self.pin_response(pin_number, pin_config)
            return pin_enabled
        except Exception as e:
            print e
			
    def IN(self):     
        return self.gpio.IN

    def OUT(self):     
        return self.gpio.OUT

    def LOW(self):       
        return self.gpio.LOW

    def HIGH(self):         
        return self.gpio.HIGH

    def disables_warnings(self):        
        return self.gpio.setwarnings(False)

    def CLEAN(self):         
        print "GPIO's pa pins!"
        return self.gpio.cleanup()

    def __del__(self):
        self.CLEAN()
        
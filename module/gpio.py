#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class in Python 2.7 for incorporation of the RPi.GPIO module to control the GPIO channels of Raspberry Pi.

"""

import RPi.GPIO as GPIO

__author__ = ""
__copyright__ = ""
__email__ = ""
__status__ = "Prototype"


class PinsGPIO(object):
    
    gpio = None

    def __init__(self):
        self.gpio = GPIO
        
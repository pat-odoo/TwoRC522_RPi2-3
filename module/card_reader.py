 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class in Python 2.7 that executes a Thread for reading RFID tags.

"""

import threading
import signal
import RPi.GPIO as GPIO
from module.gpio import PinsGPIO
from time import sleep
from module.MFRC522 import MFRC522
from module.pins import PinControl


continue_reading = True


def end_read(signal,frame):
        global continue_reading
        print "Ctrl+C captured, ending read."
        continue_reading = False
        GPIO.cleanup()

        signal.signal(signal.SIGINT, end_read)

class Nfc522(object):
    
    pc = PinControl()
    # GPIO.setup(24,GPIO.OUT)    # Code For Turn ON/OFF Buzzer
    MIFAREReader = None
    RST1 = 22 #GPIO
    RST2 = 27 #GPIO
    SPI_DEV0 = '/dev/spidev0.0'
    SPI_DEV1 = '/dev/spidev0.1'

    

    def get_nfc_rfid(self, autenticacao=True):

        print "Welcome to the MFRC522 data read example"
        print "Press Ctrl-C to stop."

        MIFAREReader = MFRC522(self.RST1, self.SPI_DEV0)

        while continue_reading:

            # Scan for cards    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # If a card is found
            # if status == MIFAREReader.MI_OK:
                # print "Card detected"     
            
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:

                # Print UID
                print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
                

                # GPIO.output(24,GPIO.HIGH)   # Code For Turn ON/OFF Buzzer
                # sleep(0.1)
                # GPIO.output(24,GPIO.LOW)
                
                # This is the default key for authentication
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                
                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                # Check if authenticated
                if status == MIFAREReader.MI_OK:
                    MIFAREReader.MFRC522_Read(8)
                    MIFAREReader.MFRC522_StopCrypto1()
                else:
                    print "Authentication error"
                

class CardReader(threading.Thread):
    
    nfc = Nfc522()
    card_number = None
            
    def run(self):
        print "%s. Run... " % self.name
        self.read()
        
    def get_rfid_card_number(self):
        id = None
        try:
            while True:
                id = self.nfc.get_nfc_rfid()
                if id:
                    id = str(id).zfill(10)
                    if (len(id) >= 10):
                        self.card_number = id
                        print "Read TAG Number: "+str(self.card_number)
                        return self.card_number
                    else:
                        print "Error TAG Number: " +str(self.card_number)
                        id = None
                        return None
                else:
                    return id
        except Exception as e:
            print e
            
    def read(self):
        try:
            self.get_rfid_card_number()
                # self.valida_cartao(self.card_number)
            return None
        except Exception as e:
            print e
            
    # def valida_cartao(self, numero):
    #     try:
    #         print "I make interesting operations here with the tag:" + str(numero)
    #     except Exception as e:
    #         print e



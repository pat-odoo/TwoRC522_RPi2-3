#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class in Python 2.7 for RFID-RC522 module driver for reading / writing RFID / NFC tags with Raspberry Pi.
This class requires SPI-Py for Python installed from the repository:
https://github.com/lthiery/SPI-Py. - MontaVista Software, Inc., Anton Vorontsov(2007)
Repository of the original class: https://github.com/mxgxw/MFRC522-python. - Mario Gómez
Idea Behind Two RC522 : https://github.com/erivandoramos/TwoRC522RPi


Connector GPIO Pins (J8)
| #Name| #Pin  | #GPIO      |
|------|-------|------------|
| SDA  | 26/24 | GPIO 7/8   |
| SCK  | 23    | GPIO 11    |
| MOSI | 19    | GPIO 10    |
| MISO | 21    | GPIO 9     |
| IRQ  | None  | None       |
| GND  | Gnd   | Gnd        |
| RST  | 15/13 | GPIO 22/27 |
| 3.3V | 1     | 3V3        |

"""

import spi
import signal
import time
from module.pins import PinControl


class MFRC522(object):
    
    pc = PinControl()
    
    serNum          = []
    MAX_LEN         = 16
    MI_ERR          = 2
    MI_NOTAGERR     = 1
    MI_OK           = 0
    BitFramingReg   = 0x0D
    CommandReg      = 0x01
    CommIEnReg      = 0x02
    CommIrqReg      = 0x04
    ControlReg      = 0x0C
    CRCResultRegL   = 0x22
    CRCResultRegM   = 0x21
    DivIrqReg       = 0x05
    ErrorReg        = 0x06
    FIFODataReg     = 0x09
    FIFOLevelReg    = 0x0A
    ModeReg         = 0x11
    PCD_AUTHENT     = 0x0E
    PCD_CALCCRC     = 0x03
    PCD_IDLE        = 0x00
    PCD_RESETPHASE  = 0x0F
    PCD_TRANSCEIVE  = 0x0C
    PICC_ANTICOLL   = 0x93
    PICC_AUTHENT1A  = 0x60
    PICC_READ       = 0x30
    PICC_REQIDL     = 0x26
    PICC_SElECTTAG  = 0x93
    PICC_WRITE      = 0xA0
    Status2Reg      = 0x08
    TModeReg        = 0x2A
    TPrescalerReg   = 0x2B
    TReloadRegH     = 0x2C
    TReloadRegL     = 0x2D
    TxAutoReg       = 0x15 
    TxControlReg    = 0x14
    
    def __init__(self, gpio, dev, spd=1000000):
        spi.openSPI(device=dev,speed=spd)
        self.NRSTPD = self.pc.read(gpio)['gpio']
        self.MFRC522_Init()
      
    def MFRC522_Init(self):
        self.pc.updates(self.NRSTPD, self.pc.HIGH())
        self.MFRC522_Reset();
        
        self.Write_MFRC522(self.TModeReg, 0x8D)
        self.Write_MFRC522(self.TPrescalerReg, 0x3E)
        self.Write_MFRC522(self.TReloadRegL, 30)
        self.Write_MFRC522(self.TReloadRegH, 0)
        self.Write_MFRC522(self.TxAutoReg, 0x40)
        self.Write_MFRC522(self.ModeReg, 0x3D)
        
        self.AntennaOn()
    
    def MFRC522_Reset(self):
        self.Write_MFRC522(self.CommandReg, self.PCD_RESETPHASE)
    
    def Write_MFRC522(self, addr, val):
        spi.transfer(((addr<<1)&0x7E,val))
    
    def Read_MFRC522(self, addr):
        val = spi.transfer((((addr<<1)&0x7E) | 0x80,0))
        return val[1]
    
    def SetBitMask(self, reg, mask):
        tmp = self.Read_MFRC522(reg)
        self.Write_MFRC522(reg, tmp | mask)
        
    def ClearBitMask(self, reg, mask):
        tmp = self.Read_MFRC522(reg);
        self.Write_MFRC522(reg, tmp & (~mask))
        
    def AntennaOn(self):
        temp = self.Read_MFRC522(self.TxControlReg)
        if(~(temp & 0x03)):
            self.SetBitMask(self.TxControlReg, 0x03)
            
    def AntennaOff(self):
        self.ClearBitMask(self.TxControlReg, 0x03)
        
    def MFRC522_ToCard(self,command,sendData):
        backData = []
        backLen = 0
        status = self.MI_ERR
        irqEn = 0x00
        waitIRq = 0x00
        lastBits = None
        n = 0
        i = 0
        
        if command == self.PCD_AUTHENT:
            irqEn = 0x12
            waitIRq = 0x10
        if command == self.PCD_TRANSCEIVE:
            irqEn = 0x77
            waitIRq = 0x30
        
        self.Write_MFRC522(self.CommIEnReg, irqEn|0x80)
        self.ClearBitMask(self.CommIrqReg, 0x80)
        self.SetBitMask(self.FIFOLevelReg, 0x80)
        
        self.Write_MFRC522(self.CommandReg, self.PCD_IDLE);  
        
        while(i<len(sendData)):
            self.Write_MFRC522(self.FIFODataReg, sendData[i])
            i = i+1
            
        self.Write_MFRC522(self.CommandReg, command)
          
        if command == self.PCD_TRANSCEIVE:
            self.SetBitMask(self.BitFramingReg, 0x80)
        
        i = 2000
        while True:
            n = self.Read_MFRC522(self.CommIrqReg)
            i = i - 1
            if ~((i!=0) and ~(n&0x01) and ~(n&waitIRq)):
                break
            
        self.ClearBitMask(self.BitFramingReg, 0x80)
        
        if i != 0:
            if (self.Read_MFRC522(self.ErrorReg) & 0x1B)==0x00:
                status = self.MI_OK
                
                if n & irqEn & 0x01:
                    status = self.MI_NOTAGERR
                
                if command == self.PCD_TRANSCEIVE:
                    n = self.Read_MFRC522(self.FIFOLevelReg)
                    lastBits = self.Read_MFRC522(self.ControlReg) & 0x07
                    if lastBits != 0:
                        backLen = (n-1)*8 + lastBits
                    else:
                        backLen = n*8
                    if n == 0:
                        n = 1
                    if n > self.MAX_LEN:
                        n = self.MAX_LEN
                    i = 0
                    while i<n:
                        backData.append(self.Read_MFRC522(self.FIFODataReg))
                        i = i + 1;
            else:
                status = self.MI_ERR
        return (status,backData,backLen)
    
    
    def MFRC522_Request(self, reqMode):
        status = None
        backBits = None
        TagType = []
        self.Write_MFRC522(self.BitFramingReg, 0x07)
        
        TagType.append(reqMode);
        (status,backData,backBits) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, TagType)
        if ((status != self.MI_OK) | (backBits != 0x10)):
            status = self.MI_ERR
            
        return (status,backBits)
    
    def MFRC522_Anticoll(self):
        backData = []
        serNumCheck = 0
        serNum = []
        self.Write_MFRC522(self.BitFramingReg, 0x00)
        serNum.append(self.PICC_ANTICOLL)
        serNum.append(0x20)
        
        (status,backData,backBits) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE,serNum)
        
        if(status == self.MI_OK):
            i = 0
            if len(backData)==5:
                while i<4:
                    serNumCheck = serNumCheck ^ backData[i]
                    i = i + 1
                if serNumCheck != backData[i]:
                    status = self.MI_ERR
            else:
                status = self.MI_ERR
                
        return (status,backData)
    
    def CalulateCRC(self, pIndata):
        self.ClearBitMask(self.DivIrqReg, 0x04)
        self.SetBitMask(self.FIFOLevelReg, 0x80);
        i = 0
        while i<len(pIndata):
            self.Write_MFRC522(self.FIFODataReg, pIndata[i])
            i = i + 1
        self.Write_MFRC522(self.CommandReg, self.PCD_CALCCRC)
        i = 0xFF
        while True:
            n = self.Read_MFRC522(self.DivIrqReg)
            i = i - 1
            if not ((i != 0) and not (n&0x04)):
                break
        pOutData = []
        pOutData.append(self.Read_MFRC522(self.CRCResultRegL))
        pOutData.append(self.Read_MFRC522(self.CRCResultRegM))
        
        return pOutData
    
    def MFRC522_SelectTag(self, serNum):
        backData = []
        buf = []
        buf.append(self.PICC_SElECTTAG)
        buf.append(0x70)
        i = 0
        while i<5:
            buf.append(serNum[i])
            i = i + 1
        pOut = self.CalulateCRC(buf)
        buf.append(pOut[0])
        buf.append(pOut[1])
        (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, buf)
        
        if (status == self.MI_OK) and (backLen == 0x18):
            # print "Size: " + str(backData[0])
            return backData[0]
        else:
            return 0
    
    def MFRC522_Auth(self, authMode, BlockAddr, Sectorkey, serNum):
        buff = []
        buff.append(authMode)
        buff.append(BlockAddr)
        
        i = 0
        while(i < len(Sectorkey)):
            buff.append(Sectorkey[i])
            i = i + 1
        i = 0
        
        while(i < 4):
            buff.append(serNum[i])
            i = i +1
            
        (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_AUTHENT,buff)
        if not(status == self.MI_OK):
            print "AUTH ERROR!"
        if not (self.Read_MFRC522(self.Status2Reg) & 0x08) != 0:
            print "AUTH ERROR(status2reg & 0x08) != 0"
        return status
    
    def MFRC522_StopCrypto1(self):
        self.ClearBitMask(self.Status2Reg, 0x08)
    
    def MFRC522_Read(self, blockAddr):
        recvData = []
        recvData.append(self.PICC_READ)
        recvData.append(blockAddr)
        pOut = self.CalulateCRC(recvData)
        recvData.append(pOut[0])
        recvData.append(pOut[1])
        (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, recvData)
        if not(status == self.MI_OK):
            print "Error in Read !"
        i = 0
        # if len(backData) == 16:
            # print "Sector "+str(blockAddr)+" "+str(backData)
    
    def MFRC522_Write(self, blockAddr, writeData):
        buff = []
        buff.append(self.PICC_WRITE)
        buff.append(blockAddr)
        crc = self.CalulateCRC(buff)
        buff.append(crc[0])
        buff.append(crc[1])
        (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, buff)
        if not(status == self.MI_OK) or not(backLen == 4) or not((backData[0] & 0x0F) == 0x0A):
            status = self.MI_ERR
            
        print str(backLen)+" dados retrospectivos &0x0F == 0x0A "+str(backData[0]&0x0F)
        if status == self.MI_OK:
            i = 0
            buf = []
            while i < 16:
                buf.append(writeData[i])
                i = i + 1
            crc = self.CalulateCRC(buf)
            buf.append(crc[0])
            buf.append(crc[1])
            (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE,buf)
            if not(status == self.MI_OK) or not(backLen == 4) or not((backData[0] & 0x0F) == 0x0A):
                print "Error writing"
            if status == self.MI_OK:
                print "Data Recorded "
    
    def MFRC522_DumpClassic1K(self, key, uid):
        i = 0
        while i < 64:
            status = self.MFRC522_Auth(self.PICC_AUTHENT1A, i, key, uid)
            # Check if authenticated
            if status == self.MI_OK:
                self.MFRC522_Read(i)
            else:
                print "Authentication error."
            i = i+1
            
    def fecha_spi(self):
        spi.closeSPI()
        print "SPI closed!"
        

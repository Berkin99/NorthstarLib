#!/usr/bin/env pythonh
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

import serial
import serial.tools.list_ports
import time
from northlib.ntrp.ntrpbuffer import NTRPBuffer

__author__ = 'Yeniay RD'
__all__ = ['NorthPort']

baudrate_e = (0,9600,19200,38400,57600,115200)

class NorthPort(): # NORTH PORT SERIAL COM
    
    AUTOBAUDRATE    = 0
    NO_CONNECTION   = 0
    READY           = 1
    BUSY            = 2
    PORTDELAY       = 0.01 #1ms Delay
    
    SYNC_DATA       = "*NC"

    def __init__(self, com=None, baudrate=AUTOBAUDRATE):
        self.mode = self.NO_CONNECTION
        self.baudrate = None
        self.com = None
        self.port = None
        self.setSerial(com,baudrate)

    def setSerial(self,com=None,baudrate=AUTOBAUDRATE):
        #Control Com and Baudrate (isAvailable)
        if not(baudrate_e.__contains__(baudrate) and (com in NorthPort.getAvailablePorts())): return
        
        if self.port != None:
            self.mode = self.NO_CONNECTION #No Connection info for Rx Thread
            self.port.close() #Need to close current active port for open new one 
        
        self.com = com
        self.baudrate = baudrate
        try:
            self.port = serial.Serial(self.com,self.baudrate,timeout=1)
            self.mode = self.READY
        except serial.SerialException as error:
            self.errorSerial() #Serial Port Problem 
    
    def readySerial(self):
        if self.port == None or self.mode==self.NO_CONNECTION: return False
        time.sleep(self.PORTDELAY)
        while self.mode == self.BUSY:
            time.sleep(self.PORTDELAY)
        return True

    def errorSerial(self):
            self.mode = self.NO_CONNECTION
            self.port = None 
            print("Serial Exception")

    def getAvailablePorts():
        return [port.device for port in serial.tools.list_ports.comports()]

    def receive(self):
        if not self.readySerial(): return None
        self.mode = self.BUSY
        try:
            if not (self.port.in_waiting > 0):
                self.mode = self.READY 
                return None  #If there is no rx data in port buffer
            msg = self.port.read(1)                         #Decode and return the data
            self.mode = self.READY
            return msg
        except serial.SerialException as error:
            self.errorSerial()
            return None
    
    def receiveLine(self):
        if not self.readySerial(): return None
        self.mode = self.BUSY
        try:
            if not (self.port.in_waiting > 0):
                self.mode = self.READY 
                return None                                 #If there is no rx data in port buffer
            msg = self.port.readline()                      #Decode and return the data
            self.mode = self.READY
            return msg
        except serial.SerialException as error:
            self.errorSerial()
            return None

    def transmit(self, msg):
        if not self.readySerialSerial(): return None
        self.mode = self.BUSY
        self.port.write(msg)
        self.mode = self.READY
    
    def destroy(self):
        self.mode = self.NO_CONNECTION
        if self.port != None:
            self.port.close()



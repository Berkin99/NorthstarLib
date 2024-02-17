#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

import threading
import serial
import time
from northbuffer import *

class NorthPort(): # NORTH PORT SERIAL COM
    
    NO_CONNECTION = 0
    TX_MODE = 1
    RX_MODE = 2
    # Baudrate Enum
    baudrate_e = (9600,19200,38400,57600,115200)

    def __init__(self, com=None, baudrate=9600):
        self.mode = self.NO_CONNECTION
        self.baudrate = None
        self.com = None
        self.port = None
        self.isActive = True
        self.buffer= NorthBuffer(10)
        self.setSerial(com,baudrate)
        #Rx Thread Loop
        self.rxThread = threading.Thread(target=self.rxProcess,daemon=False)
        self.rxThread.start()

    def setSerial(self,com=None,baudrate=9600):
        #Control Com and Baudrate (isAvailable)
        if not(self.baudrate_e.__contains__(baudrate) and (com in self.getAvailablePorts())): return
        
        if self.port != None:
            self.mode = self.NO_CONNECTION #No Connection info for Rx Thread
            self.port.close() #Need to close current active port for open new one 
        
        self.com = com
        self.baudrate = baudrate
        try:
            self.port = serial.Serial(self.com,self.baudrate,timeout=1)
            self.mode = self.RX_MODE 
        except serial.SerialException as error:
            self.errorSerial() #Serial Port Problem 
    
    def errorSerial(self):
            self.mode = self.NO_CONNECTION
            self.port = None 
            print("Serial Exception")
            if self.portErrorCallback != None: self.portErrorCallback()

    def getAvailablePorts(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def receive(self):
        if (self.port == None or self.mode==self.NO_CONNECTION): return None
        try:
            if not (self.port.in_waiting > 0): return None  #If there is no rx data in port buffer
            return self.port.readline().decode("ascii") #Decode and return the data
        except serial.SerialException as error:
            self.errorSerial()
            return None

    def transmit(self, message):
        if (self.port == None or self.mode==self.NO_CONNECTION): return

        self.mode = self.TX_MODE #TX mode info suspends the Rx Thread
        self.port.write(message.encode())
        self.mode = self.RX_MODE #Resume Rx Thread

    def rxProcess(self):
        # Rx Thread loop is available while
        # self.mode is RX_MODE
        # self.isActive is True 
        # Read data continuously and callback when data is ready
        while self.isActive:
            if self.mode != self.RX_MODE:
                time.sleep(0.1) 
                continue
            msg = self.receive()
            if msg != None:
                self.buffer.append(msg)

    def destroy(self):
        # Destroy the Rx Thread
        # Close the Serial Port
        self.isActive = False
        if self.port != None:
            self.port.close()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

from northlib.ntrp.ntrpbuffer import NTRPBuffer
from northlib.ntrp.ntrpstack import NTRPCoder
from northlib.ntrp.ntrpstack import NTRPPacket
from northlib.ntrp.northport import NorthPort
from northlib.ntrp.northradio import NorthRadio

__author__ = 'Yeniay RD'
__all__ = []

import serial
import serial.tools.list_ports
import time

class RadioManager():
    def __init__(self) -> None:
        self.availableRadios = []
        self.isInit = False

    def radioSearch(self):
        if self.isInit: return
        coms = NorthPort.getAvailablePorts()
        print(coms)
        for com in coms:
            ser = serial.Serial()
            ser.port = com
            ser.baudrate = 115200 
            ser.timeout = 1
            ser.open()
            testdata = ser.read(8).decode()
            if NorthPort.SYNC_DATA in testdata:
                print('NorthRadio found : '+com)
                ser.write("O".encode())
                ser.close()
                self.availableRadios.append(NorthRadio(com))

        self.isInit = True

    def radioClose(self):
        for radio in self.availableRadios:
            radio.destroy()
        self.availableRadios.clear()
        self.isInit = False
    




#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

import northlib.ntrp.ntrp as ntrp
from northlib.ntrp.ntrpbuffer import NTRPBuffer
from northlib.ntrp.northport import NorthPort
from northlib.ntrp.northradio import NorthRadio
from northlib.ntrp import*

__author__ = 'Yeniay RD'
__all__ = []

import serial
import serial.tools.list_ports
import time

availableRadios = []

def radioSearch():
    closeAvailableRadios()
    coms = NorthPort.getAvailablePorts()
    print("RadioManager : COM LIST = ", coms)

    for com in coms:
        ser = serial.Serial(com,NorthRadio.DEFAULT_BAUD,timeout=3)
        testdata = ""
        while 1:
            try:
                if(ser.in_waiting>6):
                    testdata = ser.read(6).decode()
                    break;
            except UnicodeDecodeError as e:
                continue

        if ntrp.NTRP_SYNC_DATA in testdata:
            print('RadioManager found : '+ com)
            ser.read_all()
            ser.close()
            availableRadios.append(NorthRadio(com))

def closeAvailableRadios():
    for radio in availableRadios:
        radio.destroy()
    availableRadios.clear()

def getAvailableRadios():
    return availableRadios



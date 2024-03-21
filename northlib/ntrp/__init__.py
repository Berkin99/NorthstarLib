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
    #Radio Search closes all radios in the list
    closeAvailableRadios()
    coms = NorthPort.getAvailablePorts()
    print("RadioManager:/COM LIST> ", coms)

    for com in coms:
        nr = None
        try:
            nr = NorthRadio(com)
            if nr.syncRadio(2):
                print('RadioManager:/> NTRP Radio found : '+ com)
                availableRadios.append(nr)
            else: nr.destroy()
        except: serial.SerialException
        
def closeAvailableRadios():
    #Reset the radios list
    for radio in availableRadios:
        radio.destroy()
    availableRadios.clear()

def getRadio(index=int)->NorthRadio:
    if index+1<len(availableRadios): return None
    return availableRadios[index]

def getAvailableRadios():
    return availableRadios



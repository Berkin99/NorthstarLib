#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

import sys
sys.path.append('./')

import time
import northlib.ntrp as radioManager
from   northlib.ntrp.northpipe import NorthPipe,NorthNRF
import northlib.ntrp.ntrp as ntrp
import northlib.ncmd.controller as ncmd
from   northlib.ncmd.northcom import NorthCOM
from   northlib.ncmd.nrxtable import NrxTableLog
import keyboard

uri =  "radio:/0/76/2/E7E7E7E301"

def uavctrlTask(uavcom):
    while 1:
        uavcom.txCMD(channels=ctrl.getAxis(),force=True)
        time.sleep(0.02)

if __name__ == '__main__':

    radioManager.radioSearch(baud=2000000)    #Arduino DUE (USB Connection) has no Baudrate
    if not len(radioManager.availableRadios) > 0: sys.exit()

    ctrl = ncmd.Controller(True) #Joystick controller
    time.sleep(1)
    if ctrl.isAlive == False : sys.exit()

    uavcom = NorthCOM(uri=uri)
    uavcom.connect()        # Request ACK to sended MSG
    uavcom.synchronize()    # Syncronize the NRX Table

    # ctrl.callBack = lambda x : uavcom.txCMD(channels=x, force= True)
    uavtable = uavcom.getParamTable()

    while 1:
        nrx_valid = False
        while (not nrx_valid):
            getval = input("> Enter Log Value: ")
            if (uavtable.search(getval) != None): nrx_valid = True

        while 1:
            if uavcom.radio.isRadioAlive() == False : break
            if keyboard.is_pressed('esc') : break 
            time.sleep(0.01)
            value = uavcom.GET(getval)        
            print(value)

        NrxTableLog(uavtable) # Print The NRX Table

    ctrl.destroy()
    uavcom.destroy()
    radioManager.closeAvailableRadios()
    
    print("UAV COMMANDER EXIT")
    sys.exit()

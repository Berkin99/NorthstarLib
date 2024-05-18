#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

import time
import sys
sys.path.append('./')

import northlib.ntrp as radioManager
from   northlib.ntrp.northpipe import NorthPipe,NorthNRF
import northlib.ntrp.ntrp as ntrp
from northlib.ncmd.northcom import NorthCOM
from northlib.ncmd.nrxtable import NrxTableLog

from liveplot import LivePlot
import keyboard

uri =  "radio:/0/76/2/E7E7E7E301"

if __name__ == '__main__':

    radioManager.radioSearch(baud=2000000)    #Arduino DUE (USB Connection) has no Baudrate
    if not len(radioManager.availableRadios) > 0: sys.exit()

    time.sleep(1)
    
    uavcom = NorthCOM(uri=uri)
    uavcom.connect()        # Request ACK to sended MSG
    uavcom.synchronize()    # Syncronize the NRX Table

    uavtable = uavcom.getParamTable()
    
    lp = LivePlot(0,100,100)
    print("Plotter Started")

    while 1:

        NrxTableLog(uavtable) # Print The NRX Table
        
        nrx_valid = False
        while (not nrx_valid):
            getval = input("> Enter Log Value: ")
            if (uavtable.search(getval) != None):
                nrx_valid = True

        minlp = int(input("> Enter min value: _"))
        maxlp = int(input("> Enter max value: _"))
        lp.set_lims(minlp,maxlp)

        while not keyboard.is_pressed('esc'):
            if uavcom.radio.isRadioAlive()==False : break 
            time.sleep(0.01)
            
            value = uavcom.GET(getval)        
            lp.add_data(value)    
            print(value)

    uavcom.destroy()
    radioManager.closeAvailableRadios()

    print("Plotter app exit")
    time.sleep(0.1)
    sys.exit()

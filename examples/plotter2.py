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

from coordinatePlotter import CoordinatePlotter
import keyboard

import threading

uri =  "radio:/0/76/2/E7E7E7E301"

def comThread(uavcom, plotter):
    uavtable = uavcom.getParamTable()
    
    while 1:
        NrxTableLog(uavtable) # Print The NRX Table
        
        nrx_valid = False
        while (not nrx_valid):
            getvalx = input("> Enter X Value: ")
            getvaly = input("> Enter Y Value: ")

            if (uavtable.search(getvalx) != None) and (uavtable.search(getvaly) != None):
                    nrx_valid = True
        while not keyboard.is_pressed('esc'):
            if uavcom.radio.isRadioAlive() == False : break 
            value = [0,0]
            time.sleep(0.01)            
            value[0] = uavcom.GET(getvalx)            
            time.sleep(0.01)
            value[1] = uavcom.GET(getvaly)
            plotter.add_coordinate(value[0],value[1])    
            print(value)

    uavcom.destroy()
    radioManager.closeAvailableRadios()
    
    print("Plotter app exit")
    time.sleep(0.1)
    sys.exit()

if __name__ == '__main__':

    radioManager.radioSearch(baud=2000000)    #(USB Connection) has no Baudrate
    if not len(radioManager.availableRadios) > 0: sys.exit()

    uavcom = NorthCOM(uri=uri)
    uavcom.connect()        # Request ACK to sended MSG
    uavcom.synchronize()    # Syncronize the NRX Table

    plotter = CoordinatePlotter(x_range=[-2.5,2.5], y_range=[-2.5,2.5])
    print("Plotter Started")

    cth = threading.Thread(target=comThread, args=(uavcom, plotter))
    cth.start()
    
    plotter.animate(1)
    cth.join()
    
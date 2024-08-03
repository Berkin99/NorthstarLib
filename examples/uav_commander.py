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

import sys
import time

import northlib.ntrp as radioManager
from northlib.ncmd.northcom import NorthCOM
from northlib.ncmd.nrxtable import NrxTableLog

uri = "radio:/0/76/2/E7E7E7E301"

if __name__ == '__main__':

    radioManager.radioSearch(baud=2000000) #Arduino DUE (USB Connection) has no Baudrate
    if not len(radioManager.availableRadios) > 0: sys.exit()
    
    time.sleep(1)
    
    uavcom = NorthCOM(uri=uri)
    uavcom.connect()
    uavcom.synchronize()
    
    time.sleep(1)
    NrxTableLog(uavcom.paramtable)

    time.sleep(5)
    while uavcom.radio.isRadioAlive():
        vector = uavcom.GET("position.z")
        print(vector)
        time.sleep(0.01)
    
    uavcom.destroy()
    radioManager.closeAvailableRadios()
    sys.exit()

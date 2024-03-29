
import sys
import time

import northlib.ntrp as radioManager
from   northlib.ntrp.ntrpbuffer import NTRPBuffer
from   northlib.ntrp.northradio import NorthRadio
from   northlib.ntrp.northpipe import NorthPipe,NorthNRF
import northlib.ntrp.ntrp as ntrp
from northlib.ncmd.northcom import NorthCOM

uri = "radio:/0/76/2/E7E7E7E301"

"""
class NTX main

"""

if __name__ == '__main__':

    radioManager.radioSearch(baud=2000000) #Arduino DUE (USB Connection) has no Baudrate
    if not len(radioManager.availableRadios) > 0: sys.exit()
    
    time.sleep(1)
    
    #rf  = NorthNRF(radioindex=0,address="E7E7E7E301")
    #rf.txTRX()
    
    uavcom = NorthCOM(uri=uri)
    uavcom.connect()
    uavcom.synchronize()
    
    print("UAV Com End.")

    # pck = ntrp.NTRPMessage('0','E')
    # pck.setHeader('MSG')
    timer = 0.0
    
    time.sleep(1)
    nx = uavcom.paramtable.getByName("CALIB.test")
    print("Found : " + str(nx.name) + " : " + "index: " + str(nx.index))
    while timer<200:
        #rf.radio.txHandler(pck=pck,receiverid='E')
        uavcom.radio.txGET(nx.index)
        print(nx.value)
        #timer+=1
        time.sleep(3)
        pass

    print("app exit")
    radioManager.closeAvailableRadios()
    sys.exit()


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
    
    rf = NorthNRF(radioindex=0,address="E7E7E7E301")

    print("UAV Com End.")

    timer = 0.0
    while timer<2000:
        rf.txMSG("Testis")

    print("app exit")
    radioManager.closeAvailableRadios()
    sys.exit()

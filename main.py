
import sys
import time

import northlib.ntrp as radioManager
from   northlib.ntrp.ntrpbuffer import NTRPBuffer
from   northlib.ntrp.northradio import NorthRadio
from   northlib.ntrp.northpipe import NorthPipe,NorthNRF
import northlib.ntrp.ntrp as ntrp

TESTMESSAGE = "Master Test Message"
"""
TOC
["name.x"]
"""

if __name__ == '__main__':

    #print(ntrp.NTRPHeader_e.OPENPIPE.value)
    #sys.exit()

    radioManager.radioSearch()
    if not len(radioManager.availableRadios) > 0: sys.exit()
    radio = radioManager.getRadio(0)
    radio.beginRadio()

    time.sleep(1)
    rfRadio = NorthNRF(0,0,address="3030303031") 
    print("RF Radio ID = " + rfRadio.id)
    
    timer = 0.0
    while timer<20:
        if(rfRadio.rxbuffer.isAvailable()):
            ntrp.NTRP_LogMessage(rfRadio.rxbuffer.read())
        time.sleep(0.001)
        timer+=0.001

    radioManager.closeAvailableRadios()

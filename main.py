
import sys
import time

import northlib.ntrp as radioManager
from   northlib.ntrp.ntrpbuffer import NTRPBuffer
from   northlib.ntrp.northradio import NorthRadio
from   northlib.ntrp.northpipe import NorthPipe,NorthNRF
import northlib.ntrp.ntrp as ntrp
import northlib.ncmd.controller as ncmd

TESTMESSAGE = "Master Test Message"

"""
class NTX main

"""

if __name__ == '__main__':

    radioManager.radioSearch(baud=2000000) #Arduino DUE (USB Connection) has no Baudrate
    if not len(radioManager.availableRadios) > 0: sys.exit()
    
    time.sleep(1)
    
    rf_pipe = NorthNRF(0,0,address="E7E7E7E301") 
    print("RF Radio ID = " + str(ord(rf_pipe.id)))
    
    
    timer = 0.0
    while timer<2000:
        #rf_pipe.radio.txHandler(ntrp.NTRPPacket('MSG'),'E',force=False)
        #rf_pipe.txMSG("Test Message")
        #time.sleep(0.001)        
        #rf_pipe.txCMD(ctrl.getAxis())
        rf_pipe.txCMD(0,[31,0,32,0])
        if(rf_pipe.rxbuffer.isAvailable()):
            ntrp.NTRP_LogMessage(rf_pipe.rxbuffer.read())   
        timer+=0.001
        #print("{:.3f}".format(timer))

    print("app exit")
    radioManager.closeAvailableRadios()
    sys.exit()

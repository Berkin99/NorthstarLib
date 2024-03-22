
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

    radioManager.radioSearch(baud=8000000) #Arduino DUE Baudrate
    if not len(radioManager.availableRadios) > 0: sys.exit()
    radio = radioManager.getRadio(0)
    radio.beginRadio()
    time.sleep(1)

    rf_pipe = NorthNRF(0,0,address="E7E7E7E300") 
    print("RF Radio ID = " + str(ord(rf_pipe.id)))
    
    #rf_pipe.txFULLTX(); #ONLY TRANSMIT MODE
    #ctrl = ncmd.Controller()

    timer = 0
    while timer<1:
        #rf_pipe.radio.txHandler(ntrp.NTRPPacket('MSG'),'E',force=True)
        #rf_pipe.txMSG("Test Message")
        #time.sleep(0.01)        
        # rf_pipe.txCMD(ctrl.getAxis())
        rf_pipe.txCMD([0,0,0,0])
        #if(rf_pipe.rxbuffer.isAvailable()):
        #    ntrp.NTRP_LogMessage(rf_pipe.rxbuffer.read())   
        
        timer+=0.004
        print(timer)

    #rf_pipe.radio.txHandler(ntrp.NTRPPacket('MSG'),'E')

    print("END")
    rf_pipe.radio.destroy()
    while 1:
        pass

    #ctrl.destroy()
    radioManager.closeAvailableRadios()
    sys.exit()

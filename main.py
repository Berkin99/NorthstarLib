
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
Test messages
MSG -> return ACK : OK
SET -> set the target data id [NEEDED TOC]
GET -> get the target data id : OK
CMD -> OK

Speed test
DS4 Controller test 
"""

if __name__ == '__main__':

    #print(ntrp.NTRPHeader_e.OPENPIPE.value)
    #sys.exit()

    radioManager.radioSearch()
    if not len(radioManager.availableRadios) > 0: sys.exit()
    radio = radioManager.getRadio(0)
    radio.beginRadio()

    time.sleep(1)
    rf_pipe = NorthNRF(0,0,address="3030303031") 
    print("RF Radio ID = " + str(ord(rf_pipe.id)))
    #ctrl = ncmd.Controller(rf_pipe)

    while 1:
        #pass
        #rf_pipe.radio.transmitNTRP(ntrp.NTRPPacket('MSG'),'E')
        rf_pipe.txMSG("Test Message")
        time.sleep(0.01)        
        #rf_pipe.txCMD(bytearray([31,62,93,0]))
        if(rf_pipe.rxbuffer.isAvailable()):
            ntrp.NTRP_LogMessage(rf_pipe.rxbuffer.read())   
        
    #ctrl.destroy()
    radioManager.closeAvailableRadios()
    sys.exit()


import sys
import time

import northlib.ntrp as radioManager
from   northlib.ntrp.ntrpbuffer import NTRPBuffer
from   northlib.ntrp.northradio import NorthRadio
from   northlib.ntrp.northpipe import NorthPipe
import northlib.ntrp.ntrp as ntrp

TESTMESSAGE = "Master Test Message"

if __name__ == '__main__':
    
    radioManager.radioSearch()
    if not len(radioManager.availableRadios) > 0: sys.exit()
    radio = radioManager.getRadio(0)
    radio.beginRadio()

    msg = ntrp.NTRPMessage()
    msg.setHeader('MSG')
    msg.dataID = len(TESTMESSAGE)
    msg.data = TESTMESSAGE.encode()

    timer = 0

    while timer<20:
        radio.transmitNTRP(msg)
        time.sleep(0.001)
        timer+=0.001

    radioManager.closeAvailableRadios()

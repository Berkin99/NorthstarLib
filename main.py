
import northlib.ntrp as rmg
from northlib.ntrp.ntrpbuffer import NTRPBuffer
from northlib.ntrp.northradio import NorthRadio
from northlib.ntrp.northpipe import NorthPipe
import northlib.ntrp.ntrp as ntrp
import sys
import time

TESTMESSAGE = "Computer Message"

def radioRouter():    
    rmg.radioSearch()
    
def radioDirect():    
    radio = NorthRadio('COM6',9600)
    rmg.availableRadios.append(radio)

if __name__ == '__main__':
    radioDirect()
    if not rmg.availableRadios[0].beginRadio() :  sys.exit()

    time.sleep(2) 
    mainpipe = NorthPipe(radio=rmg.availableRadios[0])
    mainpipe.subPipe()

    #mainpipe.transmitMSG(TESTMESSAGE)
    mainpipe.transmitGET(1)
    
    time.sleep(1)
    # while 1:
    #     if mainpipe.buffer.isAvailable()>0:
    #         ntrp.NTRP_LogMessage(mainpipe.buffer.read())

    rmg.closeAvailableRadios()

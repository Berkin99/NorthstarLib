
import northlib.ntrp
from northlib.ntrp import RadioManager
from northlib.ntrp.northport import NorthPort
from northlib.ntrp.northradio import NorthRadio
import northlib.ntrp.ntrp as ntrp

import time
import binascii



def realtest(byt):    
    rmg = RadioManager()
    rmg.radioSearch()
    time.sleep(0.1)
    if len(rmg.availableRadios)<1: return
    radio = rmg.availableRadios[0]
    radio.port.write(byt)
    radio.port.write(byt)
   
    time.sleep(0.5)
    rmg.radioClose()

def simtest(byt):
    msg = binascii.hexlify(byt)

    txt = "/x"
    ct = 0
    for ch in msg:
        if ct == 2: 
            txt += "/x"
            ct = 0
        txt += chr(ch).upper()
        ct+=1

    print(txt)



if __name__ == '__main__':

    packet = ntrp.NTRPMessage()
    packet.receiver = '0'
    packet.setHeader('CMD')
    packet.dataID = 1
    packet.data = [0]
    byt = ntrp.NTRP_Unite(packet)

    realtest(byt)

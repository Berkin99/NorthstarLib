
import northlib.ntrp
from northlib.ntrp import RadioManager
from northlib.ntrp.northport import NorthPort
from northlib.ntrp.northradio import NorthRadio
from northlib.ntrp import ntrpstack as nt

import time
import binascii



def realtest(byt):    
    rmg = RadioManager()
    rmg.radioSearch()
    time.sleep(0.1)
    radio = rmg.availableRadios[0]
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

    packet = nt.NTRPPacket()
    packet.receiver = '0'
    packet.header = nt.NTRPHeader_e.R_EXIT
    packet.dataID = ord('1')
    packet.data = [0]

    byt = nt.NTRPCoder.encode(packet)

    simtest(byt)

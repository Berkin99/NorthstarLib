
import northlib.ntrp
from northlib.ntrp import RadioManager
from northlib.ntrp.northport import NorthPort
from northlib.ntrp.northradio import NorthRadio
from northlib.ntrp import ntrpstack as nt

import time
import binascii

if __name__ == '__main__':

    packet = nt.NTRPPacket()
    packet.setHeader('CMD')
    packet.data = [255,55,44,34]
    byt = nt.NTRPCoder.encode(packet)
    
    # msg = ':'.join(hex(ord(x))[2:] for x in msg)
    # print(msg)


    rmg = RadioManager()
    rmg.radioSearch()
    time.sleep(1)
    radio = rmg.availableRadios[0]
    radio.port.write(byt)

    time.sleep(1)
    rmg.radioClose()
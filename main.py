
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
    packet.setHeader('QUAD8')
    packet.data = [255,32,33,34]
    msg = nt.NTRPCoder.encode(packet)

    msg = ':'.join(hex(ord(x))[2:] for x in msg)
    print(msg)
    #nt.NTRPCoder.encode(packet)
    # rmg = RadioManager()
    # rmg.radioSearch()
    # time.sleep(2)
    # rmg.radioClose()
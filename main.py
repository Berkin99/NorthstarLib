
import northlib.ntrp
from northlib.ntrp import RadioManager
from northlib.ntrp.northport import NorthPort
from northlib.ntrp.northradio import NorthRadio
import northlib.ntrp.ntrp as ntrp

import time
import binascii


def radioRouter(byt):
    # rmg = RadioManager()
    # rmg.radioSearch()
    # time.sleep(0.1)
    # if len(rmg.availableRadios)<1: return
    # radio = rmg.availableRadios[0]
    pass

def radioDirect(byt):    
    radio = NorthRadio('COM6',9600)
    radio.beginRadio()
    radio.transmit(byt)
    time.sleep(60)
    radio.destroy()

def byteprint(byt):
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


testmessage = "Computer Message"

if __name__ == '__main__':

    packet = ntrp.NTRPMessage()
    packet.receiver = 'X'
    packet.setHeader('GET')
    # packet.dataID = testmessage.__len__()
    # packet.data = testmessage.encode()
    packet.dataID = 1
    packet.data.append(99)
    byt = ntrp.NTRP_Unite(packet)
    

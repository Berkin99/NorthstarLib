
import northlib.ntrp as rmg
from northlib.ntrp.ntrpbuffer import NTRPBuffer
from northlib.ntrp.northradio import NorthRadio
import northlib.ntrp.ntrp as ntrp

import time
import binascii


def radioRouter(byt):    
    rmg.radioSearch()
    if rmg.availableRadios[0] == None: return

def radioDirect(byt):    
    radio = NorthRadio('COM6',9600)
    radio.beginRadio()
    radio.transmit(byt)
    time.sleep(60)
    radio.destroy()



testmessage = "Computer Message"

if __name__ == '__main__':

    buf = NTRPBuffer(20)

    packet = ntrp.NTRPMessage()
    packet.receiver = 'X'
    packet.setHeader('GET')
    # packet.dataID = testmessage.__len__()
    # packet.data = testmessage.encode()
    packet.dataID = 1
    packet.data.append(99)
    # byt = ntrp.NTRP_Unite(packet)

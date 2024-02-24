
import northlib.ntrp.ntrp as ntrp
from northlib.ntrp.ntrpbuffer import NTRPBuffer
from northlib.ntrp.northradio import NorthRadio

__author__ = 'Yeniay RD'
__all__ = ['NorthPipe','NorthNRF']


class NorthPipe():
    def __init__(self, radio = NorthRadio):
        self.id = 'X'                    #uavID
        self.radio = radio                 
        self.buffer = NTRPBuffer(10)
        self.txpck = ntrp.NTRPPacket()
    
    def txpck(self, header):
        self.txpck = ntrp.NTRPPacket()
        self.txpck.setHeader(header)

    def transmitNAK(self):               
        self.txpck = self.txpck('NAK')
        self.radio.transmitNTRP(self.txpck,self.id)     

    def transmitACK(self):
        self.txpck = self.txpck('ACK')
        self.radio.transmitNTRP(self.txpck,self.id)     

    def transmitMSG(self,msg=str):        
        self.txpck = self.txpck('MSG')
        self.txpck.data = msg.encode()
        self.txpck.dataID = len(self.txpck.data)        
        self.radio.transmitNTRP(self.txpck,self.id)     




bandwidth_e = (250,1000,2000) #kbps



class NorthNRF(NorthPipe):
        
    NRF_250KBPS  = 250
    NRF_1000KBPS = 1000
    NRF_2000KBPS = 2000

    def __init__(self, ch = 0, bandwidth = NRF_1000KBPS, address = '300'):
        self.id = 0
        self.setCh (ch)
        self.setBandwidth(bandwidth)
        self.setAddress(address)
        self.isActive = True
    
    def setCh(self,ch):
        self.channel = ch
        return True

    def setBandwidth(self,bw):
        if not bandwidth_e.__contains__(bw): return False
        self.bandwidth = bw
        return True
    
    def setAddress(self, address):
        self.address = address

    def setid(self,index):
        self.id = index



    def destroy(self):
        #TODO: Close the port with close port message
        self.isActive = False



import northlib.ntrp.ntrp as ntrp
from northlib.ntrp.ntrpbuffer import NTRPBuffer
from northlib.ntrp.northradio import NorthRadio 
import northlib.ntrp as nt

__author__ = 'Yeniay RD'
__all__ = ['NorthPipe','NorthNRF']

class NorthPipe():

    def __init__(self, _id = 'X', radio = NorthRadio):
        self.id = _id                    #uavID
        self.radio = radio                 
        self.buffer = NTRPBuffer(10)
        self.txpck = ntrp.NTRPPacket()
    
    def append(self,msg):
        self.buffer.append(msg)

    def subPipe(self,identify=False):
        index = self.radio.subPipe(self)
        if identify: self.id = index

    def txpacket(self, header):
        txpk = ntrp.NTRPPacket()
        txpk.setHeader(header)
        return txpk

    def transmitNAK(self):               
        self.txpck = self.txpacket('NAK')
        self.radio.transmitNTRP(self.txpck,self.id)     

    def transmitACK(self):
        self.txpck = self.txpacket('ACK')
        self.radio.transmitNTRP(self.txpck,self.id)     

    def transmitMSG(self,msg=str):        
        self.txpck = self.txpacket('MSG')
        self.txpck.data = msg.encode()
        self.txpck.dataID = len(self.txpck.data)        
        self.radio.transmitNTRP(self.txpck,self.id)     

    def transmitGET(self,dataid):
        self.txpck = self.txpacket('GET')
        self.dataID = dataid
        self.radio.transmitNTRP(self.txpck,self.id)

bandwidth_e = (250,1000,2000) #kbps

class NorthNRF(NorthPipe):
        
    NRF_250KBPS  = 250
    NRF_1000KBPS = 1000
    NRF_2000KBPS = 2000

    def __init__(self,radioindex = 0, ch = 0, bandwidth = NRF_1000KBPS, address = '300'):
        super().__init__(nt.availableRadios[radioindex])
        
        self.setCh (ch)
        self.setBandwidth(bandwidth)
        self.setAddress(address)
        self.isActive = True

        self.subPipe(True)
        #self.openPipe()
    
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

    def openPipe(self):
        pass

    def destroy(self):
        #TODO: Close the port with close port message
        self.isActive = False


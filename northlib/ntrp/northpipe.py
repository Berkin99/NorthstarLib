#!/usr/bin/env pythonh
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

import time 

import northlib.ntrp.ntrp as ntrp
from northlib.ntrp.ntrpbuffer import NTRPBuffer
from northlib.ntrp.northradio import NorthRadio 
import northlib.ntrp as nt

__author__ = 'Yeniay RD'
__all__ = ['NorthPipe','NorthNRF']

class NorthPipe():

    """ 
    NorthPipe Class 
    
    >It communicates with target agent in the RF Network
    >Transmit commands
    >Receive Buffer & newdata callback

    SELF -> UART LORA MODULE 
    NRF CLASS -> NRF ROUTER
    """

    def __init__(self, pipe_id = '1', radio = NorthRadio):
        self.id = pipe_id                    # Agent ID

        # LORA >
        # The Pipe ID is should be same with target agent ID
        # RF DONGLE >
        # Agent ID is represents the rf adress when use NTRP_Router Dongle
        # Agent ID identifies the target agent when use UART Lora Module
        self.radio = radio            
        self.radio.subPipe(pipe=self)  #Subscribe to Radio

        self.rxbuffer = NTRPBuffer(20) #LIFO Ring Buffer
        self.newPacketCallBack = None
        
    def append(self,msg):
        self.rxbuffer.append(msg)
        if self.newPacketCallBack != None:
            self.newPacketCallBack() 

    def setCallBack(self, func):
        #Data Ready Callback function 
        #It blocks radio rxThread : keep it small 
        self.newPacketCallBack = func

    def waitConnection(self, timeout = 1):
        self.txMSG("ACK Request")
    
        timer = 0.0
        while(not self.rxbuffer.isAvailable() and timer<=timeout):
            time.sleep(0.001)
            timer +=   0.001
            
        if(self.rxbuffer.isAvailable() == False): return 0
        return timer

    def transmitPacket(self,txPacket = ntrp.NTRPPacket,force=False):
        #Packet with receiver ID = PIPE ID
        self.radio.txHandler(txPacket,self.id,force)     

    def txNAK(self):
        self.txpck = ntrp.NTRPPacket('NAK')
        self.transmitPacket(self.txpck)     

    def txACK(self):
        self.txpck = ntrp.NTRPPacket('ACK')
        self.transmitPacket(self.txpck)     

    def txMSG(self,msg=str):        
        self.txpck = ntrp.NTRPPacket('MSG')
        self.txpck.data = msg.encode()
        self.txpck.dataID = len(self.txpck.data)        
        self.transmitPacket(self.txpck)     

    def txGET(self,dataid=int):
        self.txpck = ntrp.NTRPPacket('GET')
        self.txpck.dataID = dataid
        self.transmitPacket(self.txpck)

    def txSET(self,dataid=int,databytes=bytearray):
        self.txpck = ntrp.NTRPPacket('SET')
        self.txpck.dataID = dataid
        self.txpck.data = databytes   
        self.transmitPacket(self.txpck)
        
    def txCMD(self,channels=bytearray):
        self.txpck = ntrp.NTRPPacket('CMD')
        self.txpck.dataID = 0
        self.txpck.data = channels   
        self.transmitPacket(self.txpck,force=False)
        
class NorthNRF(NorthPipe):
        
    """
    NorthNRF Class

    NorthNRF represents RF module on external router. 
    No use case without router.
    >OPENPIPE in the router. The PIPE ID need to be same
    with NorthPipe Object. NorthNRF requests new unique ID
    from NorthRadio for PIPE ID. 
    """
    NRF_250KBPS  = 0
    NRF_1000KBPS = 1
    NRF_2000KBPS = 2

    def __init__(self, radioindex = 0, ch = 0, bandwidth = NRF_1000KBPS, address = "E7E7E7E900"):
        super().__init__(pipe_id='0', radio=nt.getRadio(radioindex))
    
        self.channel = ch                       #int
        self.bandwidth = bandwidth              #int[0,1,2]
        self.setAddress(address)

        self.isActive = True

        #If Use NRF Router module, Agents has nrf address instead of ID
        #ID needs to be defined to identify the pipe, so get new tag from radio
        self.id = self.radio.newPipeID() #Unique ID Request
        self.txOPENPIPE()
    
    def setChannel(self,ch=0):
        self.channel = ch

    def setBandwidth(self,bw=NRF_1000KBPS):
        self.bandwidth = bw
    
    def setAddress(self, adr="E7E7E7E900"):
        self.address = bytes.fromhex(adr)
        if(len(self.address) != 5): raise ValueError() #NRF Address is 5 bytes
    
    def txOPENPIPE(self):
        packet = ntrp.NTRPPacket()
        packet.header = ntrp.NTRPHeader_e.OPENPIPE
        packet.dataID = ord(self.id)
        packet.data   = self.pipeType()
        self.radio.txHandler(packet,ntrp.NTRP_ROUTER_ID)
    
    def txCLOSEPIPE(self):
        packet = ntrp.NTRPPacket()
        packet.header = ntrp.NTRPHeader_e.CLOSEPIPE
        packet.dataID = self.id
        self.radio.txHandler(packet,ntrp.NTRP_ROUTER_ID)

    def pipeType(self):
        #NRTP_Pipe_t in the router
        arr = bytearray()
        arr.append(self.channel)    #Channelbyte
        arr.append(self.bandwidth)  #Bandwidthbyte 
        arr.extend(self.address)    #5 byte address
        return arr                  #[CH,BANDWIDTH,[0,0,0,0,1]]
        
    def destroy(self):
        self.txCLOSEPIPE()
        self.radio.unsubPipe(self.id)
        self.isActive = False


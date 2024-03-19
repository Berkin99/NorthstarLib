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

    def __init__(self, pipe_id = 'X', radio = NorthRadio):
        self.id = pipe_id                    # Agent ID

        # The Pipe ID is should be same with target agent ID
        # Agent ID is represents the rf adress when use NTRP_Router Dongle
        # Agent ID identifies the target agent when use UART Lora Module
            
        self.radio = radio            
        self.radio.subPipe(self)

        self.rxbuffer = NTRPBuffer(10)
        self.txpck = ntrp.NTRPPacket()
        self.newdata = False

    def append(self,msg):
        self.rxbuffer.append(msg)
        self.newdata = True
        
    def waitConnection(self, timeout = 0.5):
        self.transmitMSG("ACK Request")
        self.newdata = False

        timer = 0.0
        while(self.newdata == False and timer<=timeout):
            time.sleep(0.01)
            timer +=   0.01
            
        if(self.newdata == False): return 0.0
        return timer

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

    def transmitGET(self,dataid=int):
        self.txpck = self.txpacket('GET')
        self.txpck.dataID = dataid
        self.radio.transmitNTRP(self.txpck,self.id)

    def transmitSET(self,dataid=int,databytes=bytearray):
        self.txpck = self.txpacket('SET')
        self.txpck.dataID = dataid
        self.txpck.data = databytes   
        self.radio.transmitNTRP(self.txpck,self.id)
        
    def transmitCMD(self,channels=bytearray):
        self.txpck = self.txpacket('CMD')
        self.txpck.dataID = 0
        self.txpck.data = channels   
        self.radio.transmitNTRP(self.txpck,self.id)
        

class NorthNRF(NorthPipe):
        
    """
    NorthNRF Class

    NorthNRF represents RF module on external router. 
    No use case without router.
    """
    NRF_250KBPS  = 0
    NRF_1000KBPS = 1
    NRF_2000KBPS = 2

    def __init__(self, radioindex = 0, ch = 0, bandwidth = NRF_1000KBPS, address = "E7E7E7E304"):
        super().__init__(nt.availableRadios[radioindex])
        
        self.channel = ch                       #int
        self.bandwidth = bandwidth              #int[0,1,2]
        self.address = bytes.fromhex(address)   #bytearray[5]
        if(len(self.address) != 5): raise ValueError()
        
        self.isActive = True

        #If Use NRF Router module, Agents has nrf address instead of ID
        #ID needs to be defined to identify the pipe, so get new tag from radio
        self.id = self.radio.newPipeID() 
        self.transmitOPENPIPE()
    
    def setChannel(self,ch):
        self.channel = ch
        return True

    def setBandwidth(self,bw):
        self.bandwidth = bw
        return True
    
    def setAddress(self, address):
        self.address = bytes.fromhex(address)

    def transmitOPENPIPE(self):
        packet = ntrp.NTRPPacket()
        packet.header = ntrp.NTRPHeader_e.OPENPIPE
        packet.dataID = self.id
        packet.data   = self.getNrfData()

        self.radio.transmitNTRP(packet,ntrp.NTRP_ROUTER_ID)
    
    def transmitCLOSEPIPE(self):
        packet = ntrp.NTRPPacket()
        packet.header = ntrp.NTRPHeader_e.CLOSEPIPE
        packet.dataID = self.id
        self.radio.transmitNTRP(packet,ntrp.NTRP_ROUTER_ID)

    def getNrfData(self):
        arr = bytearray()
        arr.append(self.channel)
        arr.append(self.bandwidth)
        arr.extend(self.address)
        return arr
        
    def destroy(self):
        self.transmitCLOSEPIPE()
        self.radio.unsubPipe(self.id)
        self.isActive = False


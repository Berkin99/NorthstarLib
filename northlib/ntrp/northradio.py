#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

import time
import threading
from northlib.ntrp.northport  import NorthPort
from northlib.ntrp.ntrpstack  import NTRPCoder
from northlib.ntrp.ntrpstack  import NTRPPacket
from northlib.ntrp.ntrpbuffer import NTRPBuffer

bandwidth_e = (250,1000,2000) #kbps

__author__ = 'Yeniay RD'
__all__ = ['NorthRadio','NorthPipe']

class NorthPipe():
    
    NRF_250KBPS  = 250
    NRF_1000KBPS = 1000
    NRF_2000KBPS = 2000

    def __init__(self, ch = 0, bandwidth = NRF_1000KBPS, address = '300'):
        self.id = 0
        self.setCh (ch)
        self.setBandwidth(bandwidth)
        self.setAddress(address)
        self.buffer = NTRPBuffer(20)
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

class NorthRadio(NorthPort):

    DEFAULT_BAUD    = 115200
    SYNC_DATA       = "*NC"
    PAIR_DATA       = "*OK"

    def __init__(self, com=None):

        super().__init__(com, self.DEFAULT_BAUD)
        self.logbuffer = NTRPBuffer(20)
        self.isSync = False
        self.pipes = []
        self.syncRadio()
        self.beginRadio()

    def syncRadio(self,timeout = 2):
        timer = 0.0
        while self.isSync == False or timer>=timeout:
            data = self.port.read(8)
            data = data.decode()
            if self.SYNC_DATA in data: self.isSync = True
            time.sleep(0.01) 
            timer += 0.01
        
        
        self.port.write(self.PAIR_DATA.encode())
        time.sleep(0.3)      #Wait remaining data
        self.port.read_all() #Clear the buffer
        
    def beginRadio(self):
        if self.mode == self.READY:
            self.isActive = True
            self.rxThread = threading.Thread(target=self.rxProcess,daemon=False)
            self.rxThread.start() 

    def openPipe(self,pipe):
        #Transmit open pipe message to dongle
        #Receive the index of pipe
        #pipe.id = 
        self.pipes.append(pipe)

    def closePipe(self,pipe):
        #Transmit close pipe message to dongle
        self.pipes.remove(pipe)

    def packetPipe(self,packet):
        sender = packet.sender
        for pipe in self.pipes:
            if sender == pipe.id:
                pipe.buffer.append(packet)
                return 
    
    def sendPipe(self,pipe,packet):
        packet.sender = 0
        packet.receiver = pipe.id
        msg = NTRPCoder.encode(packet)
        self.transmit(msg)

    def rxProcess(self):
        while self.isSync == False:
            pass
        while self.isActive:
            msg = self.receive()
            if msg == None: continue
            print(hex(ord(msg)))
            #packet = NTRPCoder.decode(msg)
            #self.packetPipe(packet)

    def destroy(self):
        self.isActive = False
        return super().destroy()

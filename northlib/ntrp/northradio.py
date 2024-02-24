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

import northlib.ntrp.ntrp as ntrp
from   northlib.ntrp.northport  import NorthPort
from   northlib.ntrp.ntrpbuffer import NTRPBuffer

__author__ = 'Yeniay RD'
__all__ = ['NorthRadio','NorthPipe']

class NorthRadio(NorthPort):

    DEFAULT_BAUD = 115200

    def __init__(self, com=None , baud=DEFAULT_BAUD):
        super().__init__(com, baud)
        self.logbuffer = NTRPBuffer(20)
        self.isSync = False
        self.pipes = []
    
    def syncRadio(self,timeout = 2):
        timer = 0.0
        msg = ''
        while self.isSync == False and timer<timeout:
            temp = self.receive()
            if temp == None:
                time.sleep(0.01) 
                timer += 0.01
                continue

            msg += chr(temp)
            if ntrp.NTRP_SYNC_DATA in msg: 
                self.isSync = True
                self.transmit(ntrp.NTRP_PAIR_DATA.encode())
                time.sleep(0.3)      #Wait remaining data
                self.port.read_all() #Clear the buffer
                return True
        return False
    
    def beginRadio(self):
        if self.mode == self.READY:
            self.isActive = True
            self.rxThread = threading.Thread(target=self.rxProcess,daemon=False)
            self.rxThread.start() 

    def transmitNTRP(self,pck=ntrp.NTRPPacket,receiver='0'):
        msg = ntrp.NTRPMessage()
        msg.talker = ntrp.NTRP_MASTER_ID
        msg.receiver = receiver 
        msg.packetsize = len(pck.data)+2

        msg.header = pck.header
        msg.dataID = pck.dataID
        msg.data = pck.data

        arr = ntrp.NTRP_Unite(msg)
        self.transmit(arr)

    def subPipe(self,pipe):
        self.pipes.append(pipe)

    def unsubPipe(self,_pipe):
        for pipe in self.pipes:
            if pipe.id == _pipe.id: self.pipes.remove(pipe)

    def rxProcess(self):        
        while self.isActive:
            byt = self.receive()
            if byt == None: continue
            if byt != ntrp.NTRP_STARTBYTE.encode(): continue
            
            arr = bytearray
            msg = None
            while(msg==None):
                arr.append(byt)
                msg = ntrp.NTRP_Parse(arr)
                byt = self.receive()

            print(ntrp.NTRP_bytes(arr))
            self.logbuffer.append(msg)


    def destroy(self):
        self.isActive = False
        return super().destroy()

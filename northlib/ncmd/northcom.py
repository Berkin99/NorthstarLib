#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

from northlib.ntrp.northpipe import NorthNRF
from northlib.ntrp.ntrpbuffer import NTRPBuffer
import northlib.ntrp.ntrp as ntrp


__author__ = 'Yeniay RD'
__all__ = ['NorthCOM']

#Uri Meaner

class NorthCOM():
    """ 
    NorthCommander Core Class
    Set URI : radio:/radioindex/ch/bandwidth/address

    Communicates with agent.
    Parameter, Function Syncronisation
    """

    CMD_PARAM_CONTENT    = 1
    CMD_FUNCTION_CONTENT = 2

    def __init__(self, uri="radio:/0/76/2/E7E7E7E301"):
        self.uri = uri
        part = uri.split('/')
        self.radio = NorthNRF(int(part[1]),int(part[2]),int(part[3]),part[4])
        self.radio.setCallBack(self.rxHandler)
        
        self.rxFunctions = {
            ntrp.NTRPHeader_e.NAK:self.rxNAK,
            ntrp.NTRPHeader_e.ACK:self.rxACK,
            ntrp.NTRPHeader_e.MSG:self.rxMSG,
            ntrp.NTRPHeader_e.CMD:self.rxCMD,
            ntrp.NTRPHeader_e.GET:self.rxGET,
            ntrp.NTRPHeader_e.SET:self.rxSET,
            ntrp.NTRPHeader_e.LOG:self.rxLOG,
            ntrp.NTRPHeader_e.RUN:self.rxRUN
        }

        self.tableReady = False
        

    def rxHandler(self,msg = ntrp.NTRPMessage):
        func = self.rxFunctions.get(msg.header.value)
        func(msg)

    def rxTable(self):
        self.radio.setRxHandleMode(self.radio.RX_HANDLE_MODE_BUFFER)
        self.radio.txCMD(dataID=self.CMD_PARAM_CONTENT)
        #While get END 
        #self.radio.txTOC()
        self.tableReady = True

    def rxNAK(self,msg):
        pass

    def rxACK(self,msg):
        pass

    def rxMSG(self,msg):
        pass

    def rxCMD(self,msg):
        pass

    def rxGET(self,msg):
        pass
        
    def rxSET(self,msg):
        #add to table of content
        pass

    def rxLOG(self,msg):
        pass

    def rxRUN(self,msg):
        pass

    def logAppend(self,parameterName):
        if self.tableReady == False : return
        pass

    def logRemove(self,parameterName):
        pass
    



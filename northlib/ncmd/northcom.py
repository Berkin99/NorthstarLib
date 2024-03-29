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
from northlib.ntrp.northpipe import NorthNRF
from northlib.ntrp.ntrpbuffer import NTRPBuffer
import northlib.ntrp.ntrp as ntrp
from northlib.ncmd.nrxtable import NrxTable

__author__ = 'Yeniay RD'
__all__ = ['NorthCOM']

#Uri Meaner


"""
class NorthTOC:
append a

"""

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
        self.radio.setRxHandleMode(self.radio.RX_HANDLE_MODE_CALLBACK)
        self.radio.txTRX()
        
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

        self.connection = False
        self.tableReady = False
        self.paramtable = NrxTable()
    
    def connect(self,timeout = 30):
        rettime = self.radio.waitConnection(timeout)
        if rettime > 0 : 
            print("NorthCom Connected : " + str(rettime))
            self.connection = True
        else: self.connection = False

    def synchronize(self):
        self.radio.setRxHandleMode(self.radio.RX_HANDLE_MODE_BUFFER)
        i=0
        miss = 0
        while 1:
            self.radio.txCMD(dataID=self.CMD_PARAM_CONTENT,channels=bytearray([i]))
            time.sleep(0.01)
            if self.radio.rxbuffer.isAvailable()<1:
                miss+=1 
                if miss > 50: print ("Too much missing command! : " + str(miss))
                continue

            msg = self.radio.rxbuffer.read()
            if not (msg.header == ntrp.NTRPHeader_e.CMD): break
            if not (msg.dataID == self.CMD_PARAM_CONTENT):break 
            self.paramtable.tableAppend(msg.data)
            i+=1

        self.tableReady = True
        self.radio.setRxHandleMode(self.radio.RX_HANDLE_MODE_CALLBACK)

    def rxHandler(self,msg = ntrp.NTRPMessage()):
        func = self.rxFunctions.get(msg.header)
        if func == None: "Packet Rx Handle Error : Header Not Found"
        func(msg)

    def rxNAK(self,msg):
        pass

    def rxACK(self,msg):
        pass

    def rxMSG(self,msg):
        pass

    def rxCMD(self,msg=ntrp.NTRPMessage()):
        if msg.dataID == self.CMD_PARAM_CONTENT:
            self.paramtable.tableAppend(msg.data)

    def rxGET(self,msg):
        pass
        
    def rxSET(self,msg=ntrp.NTRPMessage()):
        print("rxSET")
        nx = self.paramtable.getByIndex(msg.dataID)
        if nx == None: 
            print("rxSET Not found in the table : " + str(msg.dataID))
            return
        nx.setValue(msg.data)

    def rxLOG(self,msg):
        pass

    def rxRUN(self,msg):
        pass

    def logAppend(self,parameterName):
        if self.tableReady == False : return
        pass

    def logRemove(self,parameterName):
        pass
    



#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

#NCODE PROTOCOL

from enum import Enum

__author__ = 'Yeniay RD'
__all__ = ['NTRPPacket,NTRPCoder']

class NTRPHeader_e(Enum):
    NOP = 0     # No Operation
    ACK = 1     # ACK Message
    GET = 2     # GET the data address walue
    SET = 3     # SET the data address value
    MSG = 4     # Debug MSG
    CMD = 5     # COMMANDER

class NTRPType_e(Enum):
    BOOL    = 0
    INT8    = 1
    INT16   = 2
    INT32   = 3
    FLOAT   = 4
    DOUBLE  = 5
    VEC16   = 6
    VEC32   = 7
    STRING  = 8

class NTRPPacket():

    MAX_DATA_SIZE = 30

    def __init__(self):
        self.sender = '0'     #char
        self.receiver = '0'   #char

        self.header = NTRPHeader_e.NOP
        self.type = NTRPType_e.BOOL

        self.varID = 0      #int
        self.data = []      #BYTES
        self.size = 0

    def setAddress(self,address):
        self.address = address
    
    def setChannel(self,channel):
        self.ch = channel

    def setHeader(self,header):
        if not NTRPHeader_e.__contains__(header): return 
        self.header = header

    def setType(self,type):
        if not NTRPType_e.__contains__(type): return 
        self.type = type
    
    def setVarID(self,id):
        self.varID = id




def uniteCMD(packet):
    packed = chr(packet.data[0])
    return 
    pass

uniteDict = {
    'CMD' : uniteCMD
}

class NTRPCoder():

    NTRP_START  = '*'
    NTRP_END    = '\n'

    NTRP_SENDER_INDEX   = 0x01
    NTRP_RECEIVER_INDEX = 0x02
    NTRP_HEADER_INDEX   = 0x03
    NTRP_TYPE_INDEX     = 0x04
    NTRP_DATAID_INDEX   = 0x05
    NTRP_PAYLOAD_INDEX  = 0x06

    def unite(packet):
        uniteDict[packet.header.name](packet)

    def encode(packet):
        msg = NTRPCoder.NTRP_START        
        msg += str(packet.sender)
        msg += str(packet.receiver)
        msg += chr(packet.header)
        msg += NTRPCoder.unite(packet)
        return msg

    def decode(msg):
        pass
    



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
    NAK = 0     # No Operation
    ACK = 1     # ACK Message
    GET = 2     # GET the data address walue
    SET = 3     # SET the data address value
    MSG = 4     # Debug MSG
    CMD = 5     # COMMANDER
    R_OPENPIPE    = 6
    R_CLOSEPIPE   = 7
    R_EXIT        = 8 

class NTRPPacket():

    MAX_DATA_SIZE = 27

    def __init__(self):
        self.sender      = '0'          #char
        self.receiver    = '0'          #char
        self.payloadsize =  0    #payload_size

        #payloadstart
        self.header  = NTRPHeader_e.NAK     #cmd or routercmd
        self.dataID  = 0                    #data id or pipeno
        self.data    = bytearray()          #payload
        #payloadstop

    def setHeader(self,headername):
        for header in NTRPHeader_e:
            if header.name == headername:        
                self.header = header

    def setDataID(self,dataid):        
        self.dataID = dataid
    

class NTRPCoder():

    NTRP_START  = '*'
    NTRP_END    = '\n'

    NTRP_SENDER_INDEX       = 0x01
    NTRP_RECEIVER_INDEX     = 0x02
    NTRP_PAYLOADSIZE_INDEX  = 0x03

    def unite(packet):
        payload =  chr(packet.header.value)
        payload += chr(packet.dataID)
        for byte in bytearray(packet.data):
            payload += chr(byte)
        return payload 

    def encode(packet):
        msg = NTRPCoder.NTRP_START          # '*'
        msg += str(packet.sender)           # '0'
        msg += str(packet.receiver)         # 'E'
        msg += chr(len(packet.data)+2)      # length
        msg += NTRPCoder.unite(packet)      # PAYLOAD
        msg += NTRPCoder.NTRP_END           # '\n'
        byt = bytearray()                   # []    
        byt.extend(map(ord, msg))           # BYTEARRAY Formatting
        return byt

    def decode(msg):
        pass
    



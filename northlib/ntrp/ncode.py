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

class Header_e(Enum):
    NOP = 0     # No Operation
    ACK = 1     # ACK Message
    GET = 2     # GET the data address walue
    SET = 3     # SET the data address value
    MSG = 4     # Debug MSG
    CMD = 5     # COMMANDER

class Data_e(Enum):
    BOOL    = 0
    INT8    = 1
    INT16   = 2
    INT32   = 3
    FLOAT   = 4
    DOUBLE  = 5
    VEC16   = 6
    VEC32   = 7

class NcodeMSG():
    
    def __init__(self):
        self.header = 0
        self.header = 0
        self.data = []
        self.type = 0 

    def vectorMSG(self,header,vec):
        self.header = self.VEC
        self.data = vec
        self.type = 0


class Ncode():

    def encode(self,msg):
        #encode
        return 
    
    def decode(self,msg):
        # IF msg[0] != '$'
        # get size
        # msg[0]
        # header
        pass

    def decodeMSG(self,MSG):
        pass
    def decodeACK(self,MSG):
        pass
    def decodePOS(self,MSG):
        pass
    def decodeMSG(self,MSG):
        pass
    def decodeMSG(self,MSG):
        pass
    def decodeMSG(self,MSG):
        pass
    def decodeMSG(self,MSG):
        pass
    
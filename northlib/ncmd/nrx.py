#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

import enum
from northlib.ntrp.northpipe import NorthNRF
from northlib.ntrp.ntrpbuffer import NTRPBuffer
import northlib.ntrp.ntrp as ntrp


__author__ = 'Yeniay RD'
__all__ = ['Nrx','NrxTable']

NRX_BYTES_MASK  = 0x03
NRX_1BYTE       = 0x00
NRX_2BYTES      = 0x01
NRX_4BYTES      = 0x02
NRX_8BYTES      = 0x03

NRX_TYPE_MASK   =  0x0F
NRX_TYPE_INT    = (0x00<<2)
NRX_TYPE_FLOAT  = (0x01<<2)

NRX_SIGNED 	    = (0x00<<3)
NRX_UNSIGNED 	= (0x01<<3)

NRX_UINT8  =(NRX_1BYTE  | NRX_TYPE_INT | NRX_UNSIGNED)
NRX_INT8   =(NRX_1BYTE  | NRX_TYPE_INT | NRX_SIGNED)
NRX_UINT16 =(NRX_2BYTES | NRX_TYPE_INT | NRX_UNSIGNED)
NRX_INT16  =(NRX_2BYTES | NRX_TYPE_INT | NRX_SIGNED)
NRX_UINT32 =(NRX_4BYTES | NRX_TYPE_INT | NRX_UNSIGNED)
NRX_INT32  =(NRX_4BYTES | NRX_TYPE_INT | NRX_SIGNED)

NRX_FLOAT  =(NRX_4BYTES | NRX_TYPE_FLOAT | NRX_SIGNED)

NRX_CORE 	= (1<<5)
NRX_RONLY 	= (1<<6)

NRX_START = 1
NRX_STOP  = 0

NRX_VARIABLE= (0x00<<7)
NRX_GROUP   = (0x01<<7)

NRX_PERSISTENT =(1<<8)


class NrxType(enum):
    UINT8      = 0,
    INT8       = 1,
    UINT16     = 2,
    INT16      = 3,
    UINT32     = 4,
    INT32      = 5,
    FLOAT      = 6,
    FUNCTION   = 7,
    GROUPSTART = 8,
    GROUPSTOP  = 9,


#CMD,1,#index1,type1,name
def NrxType(rawtype=0):
    byte = bytes([rawtype])

class Nrx:
    def __init__(self,index=0,nrx_t=NrxType,name="unknown") -> None:
        self.name  = name
        self.index = index
        self.type  = nrx_t
    
    def getName(self):
        return self.name

def NrxParse(rawarray = bytearray):
    nrxindex = rawarray[0]
    nrxtype = rawarray[1]
    nrxname = bytearray()
    for i in range(len(rawarray)-2):
        nrxname.append(rawarray[i+2])    
    nrxname = bytearray()
    return Nrx(nrxindex,nrxtype,nrxname.decode(errors='ignore'))

class NrxTable:
    def __init__(self) -> None:
        self.table    = []

    def append(self,nrxElement = Nrx):
        self.table.append = nrxElement; 

    def getNrx(self,index):
        if index >= len(self.table):return None
        return self.table[index]
    
    def setNrx(self,index,nrxElement):
        if index >= len(self.table):return 
        self.table[index] = nrxElement
        

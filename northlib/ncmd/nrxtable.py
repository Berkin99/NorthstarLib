#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

from enum import Enum
import struct

from northlib.ntrp.northpipe import NorthNRF
from northlib.ntrp.ntrpbuffer import NTRPBuffer
import northlib.ntrp.ntrp as ntrp
import northlib.ncmd.nrx as nrx

__author__ = 'Yeniay RD'
__all__ = ['NrxTable']

class NrxTable:
    def __init__(self) -> None:
        self.table      = []
        self.indexMap   = []
        self.ingroup = False

    def tableAppend(self,rawbytes):
        #print(rawbytes)
        nrxElement = nrx.NrxParse(rawbytes)
        if nrxElement.index != len(self.table): return #Append error

        """DEBUG ELEMENT
        nrx.NrxLog(nrxElement)
        """
        
        self.table.append(nrxElement)
        if self.ingroup == False: 
            self.indexMap.append(nrxElement.index)

        if nrxElement.type.varType == nrx.NrxType_e.GROUPSTART:
            self.ingroup = True
        elif nrxElement.type.varType == nrx.NrxType_e.GROUPSTOP:
            self.ingroup = False
    
    def getByIndex(self,index=int)->nrx.Nrx|None:
        if index>len(self.table): return None
        return self.table[index]
    
    def getByName(self,name = str)->nrx.Nrx:
        part = name.split('.',1)
        nx =None
        for ix in self.indexMap:
            if self.table[ix].name == part[0]:
                nx = self.table[ix]
        
        if len(part)<2: return nx 
        if nx==None: return None

        inx = nx.index+1

        while not self.table[inx].type.group:
            if self.table[inx].name == part[1]:
                return self.table[inx]
            inx+=1



def NrxTableLog(table):
    for i in range(len(table.table)):
        nrx.NrxLog(table.table[i])
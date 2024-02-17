#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

from northport import *
from ncode import * 

class NorthRadio(NorthPort):
    BAUDRATE = 115200

    def __init__(self, uri, com=None):
        super().__init__(com, self.BAUDRATE)
        self.uri = uri
        self.nrfChannel = 0

    def setUri(self, uri):
        pass

    def txCMD(self,cmd):
        #msg = ncode.encode(cmd)
        #self.transmit(msg)
        pass
    
    def rxCMD(self):
        msg = self.buffer.read()
        #return ncode.decode()
        pass

    def destroy(self):
        return super().destroy()

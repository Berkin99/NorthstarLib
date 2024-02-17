#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

from ntrp.northport import NorthPort
from ntrp.ncode import Ncode 

class NorthRadio(NorthPort):
    BAUDRATE = 115200

    def __init__(self, uri, com=None):
        super().__init__(com, self.BAUDRATE)
        self.uri = uri
        self.nrfChannel = 0

    def setUri(self, uri):
        pass

    def tx(self,cmd):
        msg = Ncode.encode(cmd)
        if msg != None:
            self.transmit(msg)
        
    def rx(self):
        msg = self.buffer.read()
        return Ncode.decode(msg)

    def destroy(self):
        return super().destroy()

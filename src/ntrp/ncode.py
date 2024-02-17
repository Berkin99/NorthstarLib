#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team

#NRF PROTOCOL: 32 Bytes
#NCODE PROTOCOL : 32 Bytes

# $HDR,xxxxx,yyyyy,zzzz\r\n
# $VEL,
# $DS4,X,Y,Z,T\r\n


# MSG [0,"TEST"]
# ACK [1,"OK"]
# POS [2,x,y,z]
# POS [2,x,y,z]
class NcodeMSG():
    MSG = 0
    ACK = 1
    VEC = 2
    CMD = 3
    INT = 4

    def vectorMSG(self,header,vec):
        pass
    def positionMSG(self,vec):
        pass
    def velocityMSG(self,vec):
        pass
    def directionMSG(self,vec):
        pass



class Ncode():
    Header={
        "MSG" : NcodeMSG.MSG, #DEBUG MESSAGE
        "ACK" : NcodeMSG.ACK, #ACK
        "VEC" : NcodeMSG.VEC, #VECTOR
        "CMD" : NcodeMSG.CMD, #Command
        "INT" : NcodeMSG.INT, #INT
    }
    
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
    